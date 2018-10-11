# Copyright (c) 2018 .decimal, Inc. All rights reserved.
# Author:   Christopher Waugh

import os.path
import sys
import requests
import copy
# sys.path.append('lib')
import lib.thinknode_worker as tn
import lib.dicom_worker as dicom_worker

def authenticate(config):
    """Authenticate with thinknode and return the session headers"""
    url = config['api_url'] + '/cas/login'
    auth_headers = { 'Authorization': "Basic '" + config['basic_user'] + "'" }
    response = requests.get(url, headers = auth_headers)
    tn.assert_success(response)
    return {'Authorization': 'Bearer: ' + response.json()['token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'}

def get_context(config, auth_headers, realm):
    """returns the context of a given realm"""
    url = config['api_url'] + '/iam/realms/' + realm + '/context'
    response = requests.get(url, headers = auth_headers)
    tn.assert_success(response)
    return response.json()['id']

def object_copy(config, auth_headers, id, a, b):
    """copy an object from one bucket to another"""
    url = config['api_url'] + '/iss/' + id + '/buckets/' + a + '?bucket=' + b
    response = requests.post(url, headers = auth_headers)
    tn.assert_success(response)
    return response.json()['id']

def record_copy_helper(config, auth_headers, api_url, context_a, context_b, parent_id, original_body, a, b):
    """
    copies a record and its object from one realm to another. Does the same for its 
    children recursively.
    """
    # Create a copy of the original object for the new record
    duplicate_object = object_copy(config, auth_headers, original_body['immutable'], 
        a['bucket'], b['bucket'])
    url = api_url + '/rks/'
    url = url + original_body['record']['account'] + '/'
    url = url + original_body['record']['app'] + '/'
    url = url + original_body['record']['name'] + '/'
    url = url + '?context=' + context_b
    # Create the new record based on the old record and the copied immutable
    data = {
        'name': original_body['name'],
        'immutable': duplicate_object,
        'active': original_body['active'],
        'private': original_body['private'],
    }
    if original_body['lock'] != 'unlocked':
        data['lock'] = original_body['lock']
    if (parent_id is not None):
        data['parent'] = parent_id
    response = requests.post(url, headers = auth_headers, json = data)
    duplicate = response.json()
    tn.assert_success(response)
    sys.stdout.write('.')
    # Recursively copy the children
    url = api_url + '/rks'
    url += '?context=' + context_a
    url += '&parent=' + original_body['id']
    children = requests.get(url, headers = auth_headers)
    for child in children.json():
        record_copy_helper(config, auth_headers, api_url, context_a, context_b, duplicate['id'], child, a, b)
    return duplicate

def record_copy_recursive(config, auth_headers, id, realm_name_a, realm_name_b):
    """
    Copy a record and its object from one realm to another. Do the same for its 
    children recursively.

    arguments:
    config -- dictionary loaded from the config file containing 'api_url' and 'basic_user'
    auth_headers -- authentication headers for HTTP requests
    id -- id of the record to be copied
    realm_name_a -- the name of the realm the record is copied *from*
    realm_name_b -- the name of the realm the record is copied *to*
    """
    api_url = config['api_url']
    context_a = get_context(config, auth_headers, realm_name_a)
    context_b = get_context(config, auth_headers, realm_name_b)
    url = api_url + '/iam/realms/' + realm_name_a
    realm_a = requests.get(url, headers = auth_headers).json()
    url = api_url + '/iam/realms/' + realm_name_b
    realm_b = requests.get(url, headers = auth_headers).json()
    url = api_url + '/rks/' + id + '?context=' + context_a
    original = requests.get(url, headers = auth_headers)
    original_body = original.json()
    result = record_copy_helper(config, auth_headers, api_url, context_a, context_b, 
        None, original_body, realm_a, realm_b)
    print()
    return result

config = tn.read_config('thinknode.cfg')
auth_headers = authenticate(config)

if len(sys.argv) < 4:
    print()
    print('    Usage: python copy_record_recursive.py record_id source_realm_name destination_realm_name')
    print()
    print('    This depends on the "api_url" and "basic_user" values from thinknode.cfg')
    print()
else:
    record_copy_recursive(config, auth_headers, sys.argv[1], sys.argv[2], sys.argv[3])