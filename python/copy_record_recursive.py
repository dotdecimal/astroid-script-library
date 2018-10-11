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
    """copies a single record and its object from one realm to another"""
    duplicate_object = object_copy(config, auth_headers, original_body['immutable'], 
        a['bucket'], b['bucket'])
    url = api_url + '/rks/'
    url = url + original_body['record']['account'] + '/'
    url = url + original_body['record']['app'] + '/'
    url = url + original_body['record']['name'] + '/'
    url = url + '?context=' + context_b
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
    # Next, recursively copy the children
    url = api_url + '/rks'
    url += '?context=' + context_a
    url += '&parent=' + original_body['id']
    children = requests.get(url, headers = auth_headers)
    for child in children.json():
        record_copy_helper(config, auth_headers, api_url, context_a, context_b, duplicate['id'], child, a, b)
    return duplicate

def record_copy_recursive(config, auth_headers, id, realm_id_a, realm_id_b):
    api_url = config['api_url']
    context_a = get_context(config, auth_headers, realm_id_a)
    context_b = get_context(config, auth_headers, realm_id_b)
    url = api_url + '/iam/realms/' + realm_id_a
    realm_a = requests.get(url, headers = auth_headers).json()
    url = api_url + '/iam/realms/' + realm_id_b
    realm_b = requests.get(url, headers = auth_headers).json()
    url = api_url + '/rks/' + id + '?context=' + context_a
    original = requests.get(url, headers = auth_headers)
    original_body = original.json()
    result = record_copy_helper(config, auth_headers, api_url, context_a, context_b, None, original_body, realm_a, realm_b)
    print()
    return result

config = tn.read_config('thinknode.cfg')
auth_headers = authenticate(config)

if len(sys.argv) < 4:
    print('Usage: copy_record_recursive object_id source_realm destination_realm')

record_copy_recursive(config, auth_headers, sys.argv[1], sys.argv[2], sys.argv[3])