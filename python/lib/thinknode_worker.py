# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     11/3/2015
# Desc:     Worker to perform request and calculation tasks on thinknode framework

import json, ast
import sys
import msgpack
import lib.decimal_logging as dl
import jsonpickle as jp
import os.path
import shutil
from datetime import datetime, timedelta

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

import requests
session = requests.Session()
session.mount('https://', MyAdapter())

#####################################################################
# thinknode get/post functions
#####################################################################

# Perform a basic get request, useful for checking if something exists
#   param config: connection settings (url and unique basic user authentication)
#   param path: url to send get request to
def get(config, path):
    post_url = config["api_url"] + path
    dl.data('get_url: ', post_url)
    res = session.get(post_url, 
        headers = {'Authorization': 'Bearer ' + config["user_token"],
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'})
    try:
        return res.json()
    except:
        return None

# Perform a basic post request
def post(config, path, content):
    url = config["api_url"] + path
    response = requests.post(url, 
        headers = {'Authorization': 'Bearer ' + config["user_token"],
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'},
        data = content)
    assert_success(response)
    try:
        return response.json()
    except:
        return None

# Perform a basic patch request
def patch(config, path, content):
    url = config["api_url"] + path
    response = requests.patch(url, 
        headers = {'Authorization': 'Bearer ' + config["user_token"],
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'},
        data = content)
    assert_success(response)

def get_thinknode_usage(config):
    dl.event('get_usage')
    # url = config["api_url"] + '/ams/accounts/' + config["account_name"] + '/usage?include_users=true&month=201604'
    url = config["api_url"] + '/ams/accounts/' + config["account_name"] + '/usage?include_users=true'
    dl.debug(url)
    res = session.get(url, 
        headers = {'Authorization': 'Bearer ' + config["user_token"], 'content-type': 'application/json'})
    assert_success(res)
    # dl.data("Response: ", res.text)
    return res.text

# Perform a basic put request, useful for updating existing data
#   param config: connection settings (url and unique basic user authentication)
#   param path: url to send put request to
#   param json_data: optional data to update in json format
def put(config, path, json_data=None):
    post_url = config["api_url"] + path
    dl.data('put_url: ', post_url)
    res = session.put(post_url, 
        data = json_data, 
        headers = {'Authorization': 'Bearer ' + config["user_token"], 'content-type': 'application/json'})
    assert_success(res)

def delete(config, path):
    delete_url = config["api_url"] + path
    res = session.delete(delete_url, 
        headers = {'Authorization': 'Bearer ' + config["user_token"], 'content-type': 'application/json'})
    assert_success(res)
    
    return str(res.status_code)

# Authenticate with thinknode and store necessary ids.
# Gets the context id for each app detailed in the thinknode config
# Gets the app version (if non defined) for each app in the realm
#   param config: connection settings (url and unique basic user authentication)
#   returns: iam dictionary
def authenticate(config):
    dl.event("Authenticating...")
    # Get context ID and app versions
    for app_name in config["apps"]:
        # Get the version if none is provided
        if config["apps"][app_name]["branch_name"] != "master":
            config["apps"][app_name]["use_branch"] = True
            dl.event("Getting " + app_name + " Branch...")
            branch_url = config["api_url"] + '/iam/realms/' + config["realm_name"] + '/branches'
            res = session.get(branch_url, 
                headers = {'Authorization': 'Bearer ' + config["user_token"]})
            assert_success(res)
            print('Branches:')
            print(res.text)
            for app in json.loads(res.text):
                if app.get('app') == app_name:
                    config["apps"][app_name]["app_branch"] = app.get('branch')
                    dl.data(app_name + ' Branch:', config["apps"][app_name]["app_branch"])

        else:
            config["apps"][app_name]["use_branch"] = False
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
        if config["apps"][app_name]["use_branch"]:
            print('Use branches for: ' + app_name)
            context_url = config["api_url"] + '/iam/realms/' + config["realm_name"] + '/context?account=' + config["account_name"] + "&app=" + app_name + "&branch=" + config["apps"][app_name]["app_branch"]
            dl.data('context_url: ', context_url)
            res = session.get(context_url, 
                headers = {'Authorization': 'Bearer ' + config["user_token"]})
            assert_success(res)
            config["apps"][app_name]["context_id"] = res.json()["id"]
            dl.data("App " + app_name + " Context ID:", config["apps"][app_name]["context_id"])
        else:
            if config["apps"][app_name]["app_version"] == "":
                dl.data("**App " + app_name, "not installed in realm, skipping.")
                continue
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
#   param force: boolean flag indicating if the calculation should be forced to rerun if it already exists
#   returns: either calculation data or id, based on return_flag. Default is ID.
def do_calculation(config, json_data, return_data=True, return_error=False, force=False):
    # Output function name for debugging
    if 'function' in json_data:
        dl.debug('do_calculation function name: ' + json_data["function"]["name"])
    # Get app name from json request
    app_name = get_name_from_data(json_data, 'app')
    dl.debug('do_calculation app name: ' + app_name)
    # Get calculation ID
    calculation_id = post_calculation(config, json_data, force)
    # Make sure calculation folder exists
    loc = sys.path[0]
    if loc[len(loc)-1] != '/':
        loc += '/'
    if not os.path.exists(loc + 'calculations' + os.sep):
        os.makedirs(loc + 'calculations' + os.sep)
    
    if not os.path.isfile(loc + 'calculations' + os.sep + calculation_id + ".txt"):
        # Get calculation Status
        return wait_for_calculation(config, app_name, calculation_id, return_data, return_error)
    else:
        dl.event("Pulling Locally Cached Calculation...")        
        f = open(loc + 'calculations' + os.sep + calculation_id + ".txt")
        data = f.read()
        # dl.data("Calculation Result: ", data)
        
        if return_data:
            return ast.literal_eval(data)
        else:
            return calculation_id

# Query thinknode calculation service for the calculation status and wait for the calculation to finish
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: app_name the calculation was posted to (used to get the calculation context id)
#   param return_data: When True the data object will be returned, when false the thinknode id for the object will be returned
#   param return_error: When False the script will exit when error is found, when True the sciprt will return the error
#   returns: either calculation data or id, based on return_flag. Default is ID.
def wait_for_calculation(config, app_name, calculation_id, return_data=True, return_error=False):
    loc = sys.path[0]
    res = get_calculation_status(config, app_name, calculation_id)
    calculating = True
    while calculating:
        res = get_calculation_status(config, app_name, calculation_id, "completed", 30)
        if "failed" in res.json():
            calculating = False
            dl.event("Getting error logs for calculation")
            # This route can only be used if the "with_logs" parameter is used in a dev realm on a calc
            # log_res = session.get(config["api_url"] + '/calc/' + calculation_id + '/logs/ERR', 
            #     headers = {'Authorization': 'Bearer ' + config["user_token"]})
            # assert_success(log_res)
            if return_error:
                return res.text
            else:
                dl.data("Error:", res.text)
                sys.exit()
        elif "calculating" in res.json():
            dl.event("Request is still calculating...")
            dl.data("response: ", res.text)
        elif "queued" in res.json():
            dl.event("Request is queued...")
            dl.data("response: ", res.text)
        elif "uploading" in res.json():
            dl.event("Request is uploading...")
            dl.data("response: ", res.text)
        else:
            calculating = False
            if return_data:
                # Get calculation Result
                dl.event("Fetching Calculation Result...")
                res = session.get(config["api_url"] + '/iss/' + calculation_id + '?context=' + config["apps"][app_name]["context_id"], 
                    headers = {'Authorization': 'Bearer ' + config["user_token"], 'accept': 'application/octet-stream'})
                    # headers = {'Authorization': 'Bearer ' + config["user_token"], 'accept': 'application/json'})
                # dl.data("Calculation Result: ", res.text)
                assert_success(res)
                decoded = msgpack.unpackb(res.content, encoding='utf-8')

                f = open(loc + os.sep + 'calculations' + os.sep + str(calculation_id) + ".txt", 'w')
                f.write(str(decoded))
                f.close()

                return decoded
            else:
                dl.event("Fetching Calculation ID...")
                return calculation_id

# Manually gets a calculation's status
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param calc_id: calculation id of whos status to get
#   param status: used for long polling when timeout > 0 (see thinknode spec for long polling)
#   param timeout: long polling timeout
#   returns: The thinknode status of the calculation after the specified timeout
def get_calculation_status(config, app_name, calculation_id, status="completed", timeout=0):
    dl.debug("get_calculation_status: " + calculation_id)
    if (timeout <= 0):
    # if (False):
        dl.event("Checking Calculation Status...")
        url = config["api_url"] + '/calc/' + calculation_id + '/status?context=' + config["apps"][app_name]["context_id"]
        print('URL: ' + url)
        res = session.get(url, 
            headers = {'Authorization': 'Bearer ' + config["user_token"]})
        dl.data("Response: ", res.text)
    else:
        # using long polling if timeout > 0
        url = config["api_url"] + '/calc/' + calculation_id + '/status/?status=' + status + '&progress=1&timeout=' + str(timeout) + '&context=' + config["apps"][app_name]["context_id"]
        print('URL: ' + url)
        res = session.get(url, 
                headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    return res

def get_calc_status(config, app_name, calculation_id):
    dl.debug("get_calculation_status: " + calculation_id)
    url = config["api_url"] + '/calc/' + calculation_id + '/status'+ '&context=' + config["apps"][app_name]["context_id"]
    print('URL: ' + url)
    res = session.get(url, 
            headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    return res

def get_calc_request(config, app_name, calculation_id):
    dl.debug("get_calculation_status: " + calculation_id)
    url = config["api_url"] + '/calc/' + calculation_id + '?context=' + config["apps"][app_name]["context_id"]
    print('URL: ' + url)
    res = session.get(url, 
            headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    return json.loads(res.text)

def head_iss_object(config, app_name, obj_id):
    dl.debug("get_calculation_status: " + calculation_id)
    url = config["api_url"] + '/iss/' + obj_id + '?context=' + config["apps"][app_name]["context_id"]
    print('URL: ' + url)
    res = session.head(url, 
            headers = {'Authorization': 'Bearer ' + config["user_token"]})
    assert_success(res)
    # print(str(res.headers))
    h = res.headers
    h['status_code'] = res.status_code
    return h

# Manually post a calculation request, while only returning the ID and not waiting for the calculation to perform
#   note: see do_calculation if you want to wait for the calculation to finish and get results
#   param config: connection settings (url, user token, and ids for context and realm)
#   param json_data: calculation request in json format
#   param force: boolean flag indicating if the calculation should be forced to rerun if it already exists
#   returns: calculation id
def post_calculation(config, json_data, force=False):
    # Get app name from json request
    app_name = get_name_from_data(json_data, 'app')
     # Get calculation ID
    dl.event("Sending Calculation...")
    url = config["api_url"] + '/calc?context=' + config["apps"][app_name]["context_id"] + "&with_logs=false"    
    if force:
        url += '&force_run=true'
    dl.debug(url + ' :: ' )
    # print(str(json_data))
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
#   param force: boolean flag indicating if the calculation should be forced to rerun if it already exists
#   param wait_for_calc: flag to force the property calculation to wait for the calculation to finish before returning the ID
#   returns: property calculation ID
def do_calc_item_property(config, prop_name, schema, ref_id, wait_for_calc=False, force=False, return_data=False):
    dl.debug('do_calc_item_property: ' + prop_name)
    prop_calc = property(value(prop_name), schema, reference(ref_id))
    dl.debug(str(prop_calc))
    prop = {} 
    if (wait_for_calc == True):
        prop = do_calculation(config, prop_calc, return_data)
    else:
        prop = post_calculation(config, prop_calc, force)        
    dl.debug(str(prop))
    prop_text = str(prop)
    if "invalid_field" in prop_text:
        dl.error('Calc failed::do_calc_item_property: invalid index')
        sys.exit()
    else:    
        dl.debug('prop: ' + prop_name + ' :: ' + str(prop))
        return prop

# Manually post a calculation request to extract an item out of an array
#   param config: connection settings (url, user token, and ids for context and realm)
#   param index: index of the array item you want to extract
#   param schema: the schema of the array items you want to extract (helper functions to generate these should be provided)
#   param ref_id: the reference id of the array in thinknode you want to extract the item from
#   param return_on_fail: flag to return on failure instead of quitting
#   param wait_for_calc: flag to force the property calculation to wait for the calculation to finish before returning the ID
#   param force: boolean flag indicating if the calculation should be forced to rerun if it already exists
#   returns: array calculation ID
def do_calc_array_item(config, index, schema, ref_id, return_on_fail=False, force=False, wait_for_calc=False):
    dl.event('get_array_item: ')
    item_calc = array_item(value(index), schema, reference(ref_id))
    dl.debug(str(item_calc))
    ai = {}
    if (wait_for_calc == True):
        ai = do_calculation(config, item_calc, False, True, force)
    else:
        ai = post_calculation(config, item_calc, force)  
    if 'failed' in ai and return_on_fail == False:
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
#   param use_msgpack: flag on whether or not to use thinknode msgpack or json data in the iss request. Default is msgpack
#   returns: iss immutable response object
def post_immutable(config, app_name, json_data, qualified_scope, use_msgpack=True):
    dl.event("Posting object to ISS...")
    # Post immutable object
    post_url = config["api_url"] + qualified_scope + '?context=' + config["apps"][app_name]["context_id"]
    dl.data('post_url: ', post_url)
    req_headers = {}
    req_data = {}
    if use_msgpack:
        dl.debug("Using msgpack to post immutable")
        req_data = msgpack.packb(json_data, use_bin_type=True)
        req_headers = {'Authorization': 'Bearer ' + config["user_token"], 'content-type': 'application/octet-stream'}
    else:
        dl.debug("Using json to post immutable")
        req_data = json.dumps(json_data)
        req_headers = {'Authorization': 'Bearer ' + config["user_token"], 'content-type': 'application/json'}
    res = session.post(post_url, 
        data = req_data,
        headers = req_headers)
    assert_success(res)
    dl.event("    Immutable id: " + res.text)
    return res

def id_post_immutable(config, app_name, json_data, qualified_scope, use_msgpack=True):
    res = post_immutable(config, app_name, json_data, qualified_scope, use_msgpack)
    obj = json.loads(res.text)
    return obj['id']

def make_named_type_scope(config, app_name, named_type):
    scope = '/iss/named/' + config["account_name"] + '/' + app_name  + '/' + named_type
    return scope

# Post immutable named_type object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param json_data: immutable object in json format
#   param obj_name: object name of app to post to
#   param use_msgpack: flag on whether or not to use thinknode msgpack or json data in the iss request. Default is msgpack
#   returns: iss immutable response object
def post_immutable_named(config, app_name, json_data, obj_name, use_msgpack=True):
    scope = '/iss/named/' + config["account_name"] + '/dosimetry' + '/' + obj_name
    return post_immutable(config, app_name, json_data, scope, use_msgpack)

# Post immutable array of objects to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param json_data: immutable array object in json format
#   param data_type: type of items within the array to post (integer, float, etc)
#   param use_msgpack: flag on whether or not to use thinknode msgpack or json data in the iss request. Default is msgpack
#   returns: iss immutable response object
def post_immutable_array_simple_type(config, app_name, json_data, data_type, use_msgpack=True):
    scope = '/iss/array/' + data_type
    return post_immutable(config, app_name, json_data, scope, use_msgpack)

    # Post immutable array of std types to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param json_data: immutable array object in json format
#   param obj_name: object name of items within the array to post
#   param use_msgpack: flag on whether or not to use thinknode msgpack or json data in the iss request. Default is msgpack
#   returns: iss immutable response object
def post_immutable_array(config, app_name, json_data, obj_name, use_msgpack=True):
    scope = '/iss/array/named/' + config["account_name"] + "/dosimetry" + "/" + obj_name
    return post_immutable(config, app_name, json_data, scope, use_msgpack)

# Post immutable object to ISS of a dependency type 
#   param config: connection settings (url, user token, and ids for context and realm)
#   param dep_app: The name of the app the data type belongs too
#   param json_data: immutable object in json format
#   param obj_name: object name of app to post to
#   param use_msgpack: flag on whether or not to use thinknode msgpack or json data in the iss request. Default is msgpack
#   returns: iss immutable response object
def post_dependency_immutable(config, dep_app, json_data, obj_name, use_msgpack=True):
    scope = '/iss/named/' + config["account_name"] + "/" + dep_app + "/" + obj_name
    return post_immutable(config, dep_app, json_data, scope, use_msgpack)

# Post immutable object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param json_data: immutable object blob in json format
#   param use_msgpack: flag on whether or not to use thinknode msgpack or json data in the iss request. Default is msgpack
#   returns: iss immutable response object
def post_blob(config, app_name, json_data, use_msgpack=True):
    scope = '/iss/blob/' + 'blob'
    return post_immutable(config, app_name, json_data, scope, use_msgpack)

# Post immutable object to ISS
#   param config: connection settings (url, user token, and ids for context and realm)
#   param app_name: name of the app to use to get the context id from the iam config
#   param obj_id: thinknode iss reference id for object to get
#   param use_msgpack: flag on whether or not to use thinknode msgpack or json data in the iss request. Default is msgpack
#   returns: iss immutable response object
def get_immutable(config, app_name, obj_id, use_msgpack=True):
    dl.event("Requesting Data from ISS...")
    url = config["api_url"] + '/iss/' + obj_id + '?context=' + config['apps'][app_name]["context_id"] #+ "&ignore_upgrades=true"
    dl.debug("iss url:" + url)
    if use_msgpack:
        dl.debug("Using msgpack to get immutable")
        res = session.get(url, 
            headers = {'Authorization': 'Bearer ' + config["user_token"], 'accept': 'application/octet-stream'})
        assert_success(res)
        decoded = msgpack.unpackb(res.content, encoding='utf-8')
        return decoded
    else:
        dl.debug("Using json to get immutable")
        res = session.get(url, 
            headers = {'Authorization': 'Bearer ' + config["user_token"], 'accept': 'application/json'})
        assert_success(res)
        return json.loads(res.text)

def get_head(config, app_name, obj_id):
    dl.event("Requesting Head Data from ISS...")
    url = config["api_url"] + '/iss/' + obj_id + '?context=' + config['apps'][app_name]["context_id"] #+ "&ignore_upgrades=true"
    dl.debug("iss url:" + url)
    res = session.head(url, 
            headers = {'Authorization': 'Bearer ' + config["user_token"], 'accept': 'application/octet-stream'})
    assert_success(res)
    print(res.headers)
    # print(json.loads(str(res)))
    return res.headers

#####################################################################
# thinknode schema type builders
#####################################################################

# Create a schema for an array of named types
#   param type_name: the named_type for the array items
def schema_array_named_type(type_name):
    return  { "array_type": { \
                "element_schema": { \
                    "named_type": { \
                        "app": "dosimetry", \
                        "name": type_name } } } }

# Create a schema for an array of standard types
#   param type_name: the standard type (number_type, string_type) for the array items
def schema_array_standard_type(type_name):
    return  { "array_type": { \
                "element_schema": { \
                    type_name: {} } } }

# Create a schema for an array of array of standard types
#   param type_name: the standard type (number_type, string_type) for the array of array of items
def schema_array_array_standard_type(type_name):
    return  { "array_type": {
                "element_schema": {
                    "array_type": {
                        "element_schema": {
                            type_name: {}
                        }
                    }
                }
            } }

# Create a schema for a named type
#   param type_name: the named_type for the schema
def schema_named_type(type_name):
    return { "named_type": { \
                "app": "dosimetry", \
                "name": type_name } }

# Create a schema for a standard type
#   param type_name: the standard type (number_type, string_type) for the schema
def schema_standard_type(type_name):
    return  { type_name: {} }

#####################################################################
# thinknode calculation request builders
#####################################################################

# Create a value request
#   param v: value (alpha numeric)
def value(v):
    return { "value": v }

# Create an optional argument request
#   param o: fully formatted item to make optional 
def some(o):
    return  { "some": o}

# Create an optional value request
#   param v: value (alpha numeric)
def optional_value(v):
    return value(some(v))

# Create a none type (i.e. an empty optional type)
none = { "none": None }

# Create a reference request.
#   param id: immutable storage id of the object
def reference(id):
    return { "reference": id }

# Create a function request.
#   param app: app name on thinknode
#   param name: function name in app manifest
#   param args: array of arguments to pass to the called function
def function(account_name, app_name, function_name, args):
    dl.debug("function: " + function_name)
    return {
        "function": { "account": account_name, "app": app_name, "name": function_name, "args": args }
    }

# Create a property function request to extract a property from an object
#   param field: the field you want to extract
#   param schema: the schema of the field you want to pull
#   param object: the item you want to pull the data from
def property(field, schema, object):
    return {
        "property": { "field": field, "schema": schema, "object": object }
    }

# Create a array item function request to extract a item from an array
#   param index: the index of the array item you want to extract
#   param schema: the schema of the item you want to pull
#   param array: the array you want to pull the data from
def array_item(index, schema, array):
    return {
        "item": { "index": index, "schema": schema, "array": array }
    }

# Create a object request
#   param schema: the schema body of object request
#   param properties: array of properties matching the schema for the request
def structure(schema, properties):
    return {
        "object": { "schema": schema, "properties": properties }
    }
    
# Create a object request for a named_type
#   param app: app name on thinknode
#   param name: function name in app manifest
#   param args: array of arguments
def structure_named_type(app, name, args):
    schema = { "named_type": { "name": name, "app": app } }
    return structure(schema, args)

# Create an array request for a named_type
#   param app: app name on thinknode
#   param item_name: name of the named_type
#   param a: array of items (can be values or references or functions)
def array_named_type(app, item_name, a):
    return { "array": \
            { "item_schema" : \
            { "named_type": { "name": item_name, "app": app } }, "items": a } }  

# Create an optional object request for a named_type
#   param account: account name on thinknode
#   param app: app name on thinknode
#   param type_name: name of the named_type
#   param data: the real object data, non-optional version (can be values or references or functions)
def optional_named_type_object(account, app, type_name, data):
    return {
        "object": {
            "schema": {
                "optional_type": {
                    "named_type": {
                        "account": account,
                        "app": app,
                        "name": type_name
                    }
                }
            },
            "properties": data
        }
    }

# Create an array request for a number type
#   param app: app name on thinknode
#   param a: array of items
def array_number_type(app, a):
    return { "array": \
            { "item_schema" : \
            { "number_type": {} }, "items": a } } 

# Create a meta request
#   param account: account name on thinknode
#   param app: app name on thinknode
#   param type_name: name of the named_type that will be returned by the meta generator
#   param generator_ref: calculation id of the meta request generation function
def meta(account, app, type_name, generator_ref):
    return {
        "meta": {
            "schema": {
                "named_type": {
                    "account": account,
                    "app": app,
                    "name": type_name
                }
            },
            "generator": {
                "reference": generator_ref
            }
        }
}

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
        return 'dosimetry'
    else:
        return get_value_by_key(obj, key)

def get_value_by_key(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = get_value_by_key(v, key)
            if item is not None:
                return item

# Get the username associated with the given session
def get_username(iam):
    return get(iam, "/cas/session")["username"]

# Get the list of apps
def get_app_list(iam):
    return get(iam, "/apm/apps")

# Get the list of versions for an app
def get_app_versions(iam, app_name):
    return get(iam, "/apm/apps/" + self.config["account"] + "/" + app_name + "/versions")

# Get the list of app versions installed in this realm
def get_installed_app_versions(iam):
    return filter(lambda v: v["status"] == "installed",
        get(iam, "/iam/realms/" + iam['realm_name'] + "/versions"))

# Get the version of a particular app that's installed in this realm
def get_installed_app_version(iam, app_name):
    versions = [v for v in get_installed_app_versions(iam)
        if v["app"] == app_name]
    try:
        return versions[0]
    except:
        return None