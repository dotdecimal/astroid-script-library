# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     09/22/2015
# Desc:     Worker to perform request and calculation tasks on thinknode framework


import json
import sys
import lib.decimal_logging as dl
import jsonpickle as jp
import os.path
import shutil
from datetime import datetime, timedelta

import requests
session = requests.Session()

#####################################################################
# thinknode get/post functions
#####################################################################

# Worker function for getting the thinknode user token.
#   param config: connection settings (url and unique basic user authentication)
def get_user_token(config):
    res = session.get(config["api_url"] + '/cas/login',
        headers = {'Authorization': 'Basic ' + config["basic_user"]})
    assert_success(res)
    config["user_token"] = res.json()["token"]

# Authenticate with thinknode and store necessary ids.
# Gets the context id for each app detailed in the thinknode config
# Gets the app version (if non defined) for each app in the realm
#   param config: connection settings (url and unique basic user authentication)
def authenticate(config):
    dl.event("Authenticating...")
    # Get user token
    get_cached_token(config)
    dl.data("User Token:", config["user_token"])
    # Get context ID and app versions
    for app_name in config["apps"]:
        # Get the version if none is provided
        if config["apps"][app_name]["app_version"] == "":
            dl.event("Getting " + app_name + " Version...")
            version_url = config["api_url"] + '/iam/realms/' + config["realm_name"] + '/versions'
            res = session.get(version_url, 
                headers = {'Authorization': 'Bearer ' + config["user_token"]})
            assert_success(res)
            for app in json.loads(res.text):
                if app.get('app') == app_name:
                    config["apps"][app_name]["app_version"] = app.get('version')
                    dl.data(app_name + ' Version:', config["apps"][app_name]["app_version"])
        # Get context ID
        dl.event("Getting Context ID...")
        context_url = config["api_url"] + '/iam/realms/' + config["realm_name"] + '/context?account=' + config["account_name"] + "&app=" + app_name + "&version=" + config["apps"][app_name]["app_version"]
        dl.data('context_url: ', context_url)
        res = session.get(context_url, 
            headers = {'Authorization': 'Bearer ' + config["user_token"]})
        assert_success(res)
        config["apps"][app_name]["context_id"] = res.json()["id"]
        dl.data("App " + app_name + " Context ID:", config["apps"][app_name]["context_id"])
    return config

# Send calculation request to thinknode and wait for the calculation to perform. Caches locally calculation results so if the same calculation is performed again, the calculation
# does not have to be repeatedly pulled from thinknode. Saves one calculation time and bandwidth.
#   note: see post_calculation if you just want the calculation ID and don't need to wait for the calculation to finish or get results
#   param config: connection settings (url, user token, and ids for context and realm)
#   param json_data: calculation request in json format
#   param return_data: When True the data object will be returned, when false the thinknode id for the object will be returned
#   param return_error: When False the script will exit when error is found, when True the sciprt will return the error
def do_calculation(config, json_data, return_data=True, return_error=False):
    # Output function name for debugging
    if 'function' in json_data:
        dl.debug('do_calculation function name: ' + json_data["function"]["name"])
    # Get app name from json request
    app_name = get_name_from_data(json_data, 'app')
    # Get calculation ID
    calculation_id = post_calculation(config, json_data)
    # Make sure calculation folder exists
    loc = sys.path[0]
    if loc[len(loc)-1] != '/':
        loc += '/'
    if not os.path.exists(loc + 'calculations' + os.sep):
        os.makedirs(loc + 'calculations' + os.sep)
    if not os.path.isfile(loc + 'calculations' + os.sep + calculation_id + ".txt"):
        # Get calculation Status
        res = get_calculation_status(config, app_name, calculation_id)
        calculating = True
        while calculating:
            res = get_calculation_status(config, app_name, calculation_id, "completed", 30)
            if res.json()["type"] == "failed":
                calculating = False
                dl.event("Getting error logs for calculation")
                log_res = session.get(config["api_url"] + '/calc/' + calculation_id + '/logs/ERR', 
                    headers = {'Authorization': 'Bearer ' + config["user_token"]})
                assert_success(res)
                if return_error:
                    return log_res.text
                else:
                    return res.text
            elif res.json()["type"] == "calculating":
                dl.event("Request is still calculating...")
                dl.data("response: ", res.text)
            elif res.json()["type"] == "queued":
                dl.event("Request is queued...")
                dl.data("response: ", res.text)
            elif res.json()["type"] == "uploading":
                dl.event("Request is uploading...")
                dl.data("response: ", res.text)
            else:
                calculating = False
                if return_data:
                    # Get calculation Result
                    dl.event("Fetching Calculation Result...")
                    res = session.get(config["api_url"] + '/iss/' + calculation_id + '/?context=' + config["apps"][app_name]["context_id"], 
                        headers = {'Authorization': 'Bearer ' + config["user_token"]})
                    # dl.data("Calculation Result: ", res.text)
                    assert_success(res)

                    f = open(loc + os.sep + 'calculations' + os.sep + str(calculation_id) + ".txt", 'a')
                    f.write(res.text)
                    f.close()

                    return json.loads(res.text)
                else:
                    dl.event("Fetching Calculation ID...")
                    return calculation_id
    else:
        dl.event("Pulling Locally Cached Calculation...")        
        f = open(loc + 'calculations' + os.sep + calculation_id + ".txt")
        data = str(f.read())
        #dl.data("Calculation Result: ", data)
        
        if return_data:
            return json.loads(data)
        else:
            return calculation_id

# Manually gets a calculation's status
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param calc_id: calculation id of whos status to get
#   param status: used for long polling when timeout > 0
#   param timeout: long polling timeout
def get_calculation_status(config, app_name, calculation_id, status="completed", timeout=0):
    if (timeout <= 0):
        dl.event("Checking Calculation Status...")
        res = session.get(config["api_url"] + '/calc/' + calculation_id + '/status?context=' + config["apps"][app_name]["context_id"], 
            headers = {'Authorization': 'Bearer ' + config["user_token"]})
        dl.data("Response: ", res.text)
    else:
        # using long polling if timeout > 0
        res = session.get(config["api_url"] + '/calc/' + calculation_id + '/status/?status=' + status + '&progress=1&timeout=' + str(timeout) + '&context=' + config["apps"][app_name]["context_id"], 
                headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    return res

# Manually post a calculation request, while only returning the ID and not waiting for the calculation to perform
#   note: see do_calculation if you want to wait for the calculation to finish and get results
#   param config: connection settings (url, user token, and ids for context and realm)
#   param json_data: calculation request in json format
def post_calculation(config, json_data):
    # Get app name from json request
    app_name = get_name_from_data(json_data, 'app')
     # Get calculation ID
    dl.event("Sending Calculation...")
    url = config["api_url"] + '/calc/?context=' + config["apps"][app_name]["context_id"]
    dl.debug(url)
    res = session.post(url, 
        data = json.dumps(json_data), 
        headers = {'Authorization': 'Bearer ' + config["user_token"], 'content-type': 'application/json'})
    assert_success(res)
    calculation_id = res.json()["id"]
    dl.data("Calculation ID: ", calculation_id)
    return calculation_id

# Manually post a calculation request to extract a property out of a 
#   param config: connection settings (url, user token, and ids for context and realm)
#   param prop_name: the name of the property you want to extract
#   param schema: the schema of the property you want to extract (helper functions to generate these should be provided)
#   param ref_id: the reference id of the object in thinknode you want to extract the property from
def do_calc_item_property(config, prop_name, schema, ref_id):
    dl.debug('do_calc_item_property: ' + prop_name)
    prop_calc = property(value(prop_name), schema, reference(ref_id))
    dl.debug(str(prop_calc))
    prop = do_calculation(config, prop_calc, False, True)
    dl.debug(str(prop))
    prop_text = str(prop)
    if "invalid_field" in prop_text:
        dl.error('Calc failed::do_calc_item_property: invalid index')
        sys.exit()
    else:    
        dl.debug('prop: ' + prop_name + ' :: ' + prop)
        return prop

# Manually post a calculation request to extract an item out of an array
#   param config: connection settings (url, user token, and ids for context and realm)
#   param index: index of the array item you want to extract
#   param schema: the schema of the array items you want to extract (helper functions to generate these should be provided)
#   param ref_id: the reference id of the array in thinknode you want to extract the item from
def do_calc_array_item(config, index, schema, ref_id):
    dl.event('get_array_item: ')
    item_calc = array_item(value(index), schema, reference(ref_id))
    ai = do_calculation(config, item_calc, False)
    if 'failed' in ai:
        dl.error('Calc failed::do_calc_array_item:invalid index')
        sys.exit()
    else:
        dl.debug('array_item: ' + str(ai))
        return ai

# Generic function to post an object to immutable storage system (ISS)
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param json_data: immutable object in json format
#   param qualified_scope: unique url for the iss type being posted (i.e. named types, blobs, arrays all have unique urls)
def post_immutable(config, app_name, json_data, qualified_scope):
    dl.event("Posting object to ISS...")
    # Post immutable object
    post_url = config["api_url"] + qualified_scope + '/?context=' + config["apps"][app_name]["context_id"]
    dl.data('post_url: ', post_url)
    res = session.post(post_url, 
        data = json.dumps(json_data), 
        headers = {'Authorization': 'Bearer ' + config["user_token"], 'content-type': 'application/json'})
    assert_success(res)
    dl.event("    Immutable id: " + res.text)
    return res

# Post immutable named_type object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param json_data: immutable object in json format
#   param obj_name: object name of app to post to
def post_immutable_named(config, app_name, json_data, obj_name):
    scope = '/iss/named/' + config["account_name"] + '/rt_types' + '/' + obj_name
    return post_immutable(config, app_name, json_data, scope)

# Post immutable array of objects to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param json_data: immutable array object in json format
#   param obj_name: object name of items within the array to post
def post_immutable_array(config, app_name, json_data, obj_name):
    scope = '/iss/array/named/' + config["account_name"] + "/rt_types" + "/" + obj_name
    return post_immutable(config, app_name, json_data, scope)

# Post immutable object to ISS of a dependency type 
#   param config: connection settings (url, user token, and ids for context and realm)
#   param dep_app: The name of the app the data type belongs too
#   param json_data: immutable object in json format
#   param obj_name: object name of app to post to
def post_dependency_immutable(config, dep_app, json_data, obj_name):
    scope = '/iss/named/' + config["account_name"] + "/" + dep_app + "/" + obj_name
    return post_immutable(config, dep_app, json_data, scope)

# Post immutable object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param json_data: immutable object blob in json format
def post_blob(config, app_name, json_data):
    scope = '/iss/blob/' + 'blob'
    return post_immutable(config, app_name, json_data, scope)

# Post immutable object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param obj_id: thinknode iss reference id for object to get
def get_immutable(config, app_name, obj_id):
    dl.event("Requesting Data from ISS...")
    url = config["api_url"] + '/iss/' + obj_id + '/?context=' + config['apps'][app_name]["context_id"]
    res = session.get(url, 
        headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    return json.loads(res.text)

#####################################################################
# thinknode schema type builders
#####################################################################

# Create a schema for an array of named types
#   param type_name: the named_type for the array items
def schema_array_named_type(type_name):
    return  { "type": "array_type", \
            "array_type": { \
                "element_schema": { \
                    "type": "named_type", \
                    "named_type": { \
                        "app": "rt_types", \
                        "name": type_name } } } }

# Create a schema for an array of standard types
#   param type_name: the standard type (number_type, string_type) for the array items
def schema_array_standard_type(type_name):
    return  { "type": "array_type", \
            "array_type": { \
                "element_schema": { \
                    "type": type_name, \
                    type_name: {} } } }

# Create a schema for an array of array of standard types
#   param type_name: the standard type (number_type, string_type) for the array of array of items
def schema_array_array_standard_type(type_name):
    return  { "array_type": {
                "element_schema": {
                    "array_type": {
                        "element_schema": {
                            type_name: {},
                            "type": type_name
                        }
                    },
                    "type": "array_type"
                }
            },
            "type": "array_type" }

# Create a schema for a named type
#   param type_name: the named_type for the schema
def schema_named_type(type_name):
    return { "type": "named_type", \
            "named_type": { \
                "app": "rt_types", \
                "name": type_name } }

# Create a schema for a standard type
#   param type_name: the standard type (number_type, string_type) for the schema
def schema_standard_type(type_name):
    return  { "type": type_name, \
            type_name: {} }

#####################################################################
# thinknode calculation request builders
#####################################################################

# Create a value request
#   param v: value (alpha numeric)
def value(v):
    return { "type": "value", "value": v }

# Create an optional argument request
#   param o: fully formatted item to make optional 
def some(o):
    return  { "type": "some", "some": o}

# Create an optional value request
#   param v: value (alpha numeric)
def optional_value(v):
    return value(some(v))

# Create a none type (i.e. an empty optional type)
none = value({ "type": "none", "none": None }) 

# Create a reference request.
#   param id: immutable storage id of the object
def reference(id):
    return { "type": "reference", "reference": id }

# Create a function request.
#   param app: app name on thinknode
#   param name: function name in app manifest
#   param args: array of arguments to pass to the called function
def function(account_name, app_name, function_name, args):
    return {
        "type": "function",
        "function": { "account": account_name, "app": app_name, "name": function_name, "args": args }
    }

# Create a property function request to extract a property from an object
#   param field: the field you want to extract
#   param schema: the schema of the field you want to pull
#   param structure: the item you want to pull the data from
def property(field, schema, structure):
    return {
        "type": "property",
        "property": { "field": field, "schema": schema, "structure": structure }
    }

# Create a array item function request to extract a item from an array
#   param index: the index of the array item you want to extract
#   param schema: the schema of the item you want to pull
#   param array: the array you want to pull the data from
def array_item(index, schema, array):
    return {
        "type": "item",
        "item": { "index": index, "schema": schema, "array": array }
    }

# Create a structure request
#   param schema: the schema body of structure request
#   param properties: array of properties matching the schema for the request
def structure(schema, properties):
    return {
        "type": "structure",
        "structure": { "schema": schema, "properties": properties }
    }
    
# Create a structure request for a named_type
#   param app: app name on thinknode
#   param name: function name in app manifest
#   param args: array of arguments
def structure_named_type(app, name, args):
    schema = { "type": "named_type", "named_type": { "name": name, "app": app } }
    return structure(schema, args)

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
#   param app: app name on thinknode
#   param a: array of items
def array_number_type(app, a):
    return { "type": "array", "array": \
            { "item_schema" : \
            { "type": "number_type", \
            "number_type": {} }, "items": a } } 

#####################################################################
# misc helpers
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
    file = open(sys.path[0] + os.sep + path)
    config = json.load(file)
    file.close()
    return config

# Worker function for getting the thinknode user token.
#   note: if you need to force a new token, delete the token.json file from the calculations directory
#   param config: connection settings (url and unique basic user authentication)
def get_cached_token(config):
    now = datetime.now()
    # Make sure calculation folder exists
    loc = sys.path[0]
    if loc[len(loc)-1] != os.sep:
        loc += '/'
    path = loc + 'calculations' + os.sep + "token.json"
    # folder not present, make it
    if not os.path.exists(loc + 'calculations' + os.sep):
        os.makedirs(loc + 'calculations' + os.sep)
    # cached token file not present, make a new one
    if not os.path.isfile(path):
        dl.event("Creating New User Token...")
        get_user_token(config)
        file = open(path, 'a')
        file.write(json.dumps({'token': config["user_token"], 'refreshed': str(now) }))
        file.close()
    else:
        file = open(path)
        user_cache = json.load(file)
        file.close()
        cached_datetime = datetime.strptime(user_cache["refreshed"], "%Y-%m-%d %H:%M:%S.%f")
        expiration_time = now - timedelta(hours=14)
        # token is old
        if (cached_datetime < expiration_time):
            dl.event("Getting New User Token...")
            get_user_token(config)
            file = open(path, 'w')
            file.write(json.dumps({'token': config["user_token"], 'refreshed': str(now) }))
            file.close()
        else:
            dl.event("Getting Cached User Token...")
            config["user_token"] = user_cache["token"]

# Clears the cached calculations in the calculation directory
def clear_calculations():
    shutil.rmtree('calculations')
    os.makedirs('calculations')
           
# Turn dosimetry_types class object into serialized json dictionary. 
# This handles interdependent classes within dosimetry_types.
#   param obj: instance of a dosimetry_types class
def to_json(obj):
    return json.loads(jp.encode(obj, unpicklable=False))

# Gets the value of the specified key from a json dict
#   param obj: Json dictionary to search
#   param key: Key to search dictionary for and whos value to return
def get_name_from_data(obj, key):
    json_string = str(obj)
    if key not in json_string:
        dl.debug(key + ' not found in data: ' + json_string)
        return 'rt_types'
    else:
        return get_value_by_key(obj, key)

def get_value_by_key(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = get_value_by_key(v, key)
            if item is not None:
                return item
