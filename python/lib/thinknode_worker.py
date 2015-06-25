# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     06/17/2015
# Desc:     Worker to perform request and calculation tasks on thinknode framework

import requests
import json
import sys
import lib.decimal_logging as dl

#####################################################################
# thinknode get/post functions
#####################################################################

# Check that the response returned a successful code
#   param res: http response
def assert_success(res):
    if res.status_code != 200:
        dl.error("Server Responded: " + str(res.status_code) + " - " + res.text)
        sys.exit()

# Read the thinknode config file
#   param path: relative location of config file
def read_config(path):
    file = open(path)
    config = json.load(file)
    file.close()
    return config

# Authenticate with thinknode and store necessary ids
#   param config: connection settings (url and unique basic user authentication)
def authenticate(config):
    dl.event("Authenticating...")
    # Get user token
    dl.event("Getting User Token...")
    res = requests.get(config["api_url"] + '/cas/login',
        headers = {'Authorization': 'Basic ' + config["basic_user"]})
    assert_success(res)
    dl.data("User Token:", res.text)
    config["user_token"] = res.json()["token"]
    # Get realm ID
    dl.event("Getting Realm ID...")
    res = requests.get(config["api_url"] + '/iam/realms', 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    dl.data("Realms:", res.text)
    realm_list = json.loads(res.text)
    for realm in realm_list:
        desc = realm['name']
        if desc == config["realm_name"]:    
            config["realm_id"] = realm['id']
            config["bucket_id"] = realm['bucket_id']
    dl.data("Realm ID:", config["realm_id"])
    # Get context ID
    dl.event("Getting Context ID...")
    res = requests.get(config["api_url"] + '/iam/realms/' + config["realm_id"] + '/contexts/' + config["app_name"] + "/" + config["app_version"], 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    config["context_id"] = res.json()["id"]
    dl.data("Context ID:", config["context_id"])
    return config

# Send calculation request to thinknode api
#   param config: connection settings (url, user token, and ids for context and realm)
#   param json_data: calculation request in json format
def do_calculation(config, json_data, return_data=True):
    # Get calculation ID
    dl.event("Sending Calculation...")
    res = requests.post(config["api_url"] + '/calc/?context=' + config["context_id"], 
        data = json.dumps(json_data), 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    calculation_id = res.json()["id"]
    dl.data("Calculation ID: ", calculation_id)
    # Get calculation Status - using long polling
    dl.event("Checking Calculation Status...")
    res = requests.get(config["api_url"] + '/calc/' + calculation_id + '/status?context=' + config["context_id"], 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    dl.data("response: ", res.text)
    res = requests.get(config["api_url"] + '/calc/' + calculation_id + '/status/?status=completed&progress=1&timeout=30', 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    if res.json()["type"] == "failed":
        dl.error("Server Responded: " + res.text)
        dl.event("Getting error logs for calculation")
        res = requests.get(config["api_url"] + '/calc/' + calculation_id + '/logs/ERR', 
            headers = {'Authorization': 'Bearer ' + config["user_token"]})
        assert_success(res)
        return res
    else:
        # Get calculation Result
        dl.event("Fetching Calculation Result...")
        res = requests.get(config["api_url"] + '/calc/' + calculation_id + '/result/?context=' + config["context_id"], 
            headers = {'Authorization': 'Bearer ' + config["user_token"]})
        assert_success(res)
        if return_data:
            return res
        else:
            return calculation_id

# Post immutable object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param json_data: immutable object in json format
#   param obj_name: object name of app to post to
def post_immutable(config, json_data, obj_name):
    dl.event("Posting object to ISS...")
    # Post immutable object
    res = requests.post(config["api_url"] + '/iss/named/' + config["app_name"] + "/" + obj_name + '/?context=' + config["context_id"], 
        data = json.dumps(json_data), 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    dl.event("    Immutable id: " + res.text)
    return res

# Post immutable object to ISS of a dependency type 
#   param config: connection settings (url, user token, and ids for context and realm)
#   param dep_app: The name of the app the data type belongs too
#   param json_data: immutable object in json format
#   param obj_name: object name of app to post to
def post_dependency_immutable(config, dep_app, json_data, obj_name):
    print("Posting object to ISS...")
    # Post immutable object
    res = requests.post(config["api_url"] + '/iss/named/' + dep_app + "/" + obj_name + '/?context=' + config["context_id"], 
        data = json.dumps(json_data), 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    print("    Immutable id: " + res.text)
    return res

# Post immutable object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param json_data: immutable object blob in json format
def post_blob(config, json_data):
    dl.event("Posting blob to ISS...")
    # Post immutable object
    res = requests.post(config["api_url"] + '/iss/blob/' + 'blob' + '/?context=' + config["context_id"], 
        data = json.dumps(json_data), 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    dl.event("    Immutable id: " + res.text)
    return res

# Post immutable object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param obj_id: thinknode iss reference id for object to get
def get_immutable(config, obj_id):
    dl.event("Requesting Data from ISS...")
    res = requests.get(config["api_url"] + '/iss/' + obj_id + '/?context=' + config["context_id"], 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    return res.text

#####################################################################
# thinknode calculation request builders
#####################################################################

# Create a value request
#   param v: value (alpha numeric)
def value(v):
    return { "type": "value", "value": v }

# Create a reference request.
#   param id: immutable storage id of the object
def reference(id):
    return { "type": "reference", "reference": id }

# Create a function request.
#   param app: app name on thinknode
#   param name: function name in app manifest
#   param args: array of arguments to pass to the called function
def function(app, name, args):
    return {
        "type": "function",
        "function": { "app": app, "name": name, "args": args }
    }

# Create a structure request for a named_type
#   param app: app name on thinknode
#   param name: function name in app manifest
#   param args: array of arguments
def structure_named_type(app, name, args):
    return {
        "type": "structure", \
        "structure": { "schema": { "type": "named_type", "named_type": { "name": name, "app": app } }, \
        "properties": args }
    }

# Create an array request for a named_type
#   param app: app name on thinknode
#   param item_name: name of the named_type
#   param a: array of items
def array_named_type(app, item_name, a):
    return { "type": "array", "array": \
            { "item_schema" : \
            { "type": "named_type", \
            "named_type": { "name": item_name, "app": app } }, "items": a } }  

# Create an array request for a named_type
#   param app: app name on thinknode
#   param item_name: name of the named_type
#   param a: array of items
def array_referenced_named_type(app, item_name, a):
    return { "type": "array", "array": \
            { "item_schema" : \
            { "type": "reference_type", \
            "reference_type": { "type": "named_type", \
            "named_type": { "name": item_name, "app": app } } }, "items": a } } 
            # { "type": "named_type", \
            # "named_type": { "name": item_name, "app": app } }, "items": a } }  


# Create an array request for a number type
def array_number_type(app, a):
#   param app: app name on thinknode
#   param a: array of items
    return { "type": "array", "array": \
            { "item_schema" : \
            { "type": "number_type", \
            "number_type": {} }, "items": a } } 

# Create a none type
none = value({ "type": "none", "none": None })