# Copyright (c) 2018 .decimal, Inc. All rights reserved.
# Author:   Christopher Waugh

import os.path
import sys
import requests
import copy
# sys.path.append('lib')
import lib.thinknode_worker as tn
import lib.dicom_worker as dicom_worker
import lib.rks_worker as rks

def authenticate(config):
    '''Authenticate with thinknode and return the session headers'''
    url = config['api_url'] + '/cas/login'
    auth_headers = { 'Authorization': "Basic '" + config['basic_user'] + "'" }
    response = requests.get(url, headers = auth_headers)
    tn.assert_success(response)
    res = copy.deepcopy(config)
    res['auth_headers'] = {'Authorization': 'Bearer: ' + response.json()['token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'}
    return res


#if len(sys.argv) < 4 :
#    print('too few args. Requires record id, source bucket, and destination bucket.')
#    exit()

def getContext(config, realm):
    '''returns the context of a given realm'''
    url = config['api_url'] + '/iam/realms/' + realm + '/context'
    response = requests.get(url, headers = config['auth_headers'])
    tn.assert_success(response)
    return response.json()['id']

def getObjectType(config, context, id):
    url = config['api_url'] + '/iss/' + id + '/' + context
    response = requests.head(url, headers = config['auth_headers'])
    tn.assert_success(response)
    result = response.json()['type']
    return result

def getVersion(config, type, realm):
    app = '/'.split(type)[2]
    url = config['api_url'] + '/realms/' + realm + '/versions'
    response = requests.get(url, headers = config['auth_headers'])
    tn.assert_success(response)
    result = response.headers['thinknode-type']
    return result
    
def getSchema(config, type, version):
    app = '/'.split(type)[2]
    schema_type = '/'.split(type)[3]
    url = (config['api_url'] + '/apm/apps/' + config['account'] + '/' + app + '/versions/' + 
        version + '?include_manifest=true')
    response = requests.get(url, headers = config['auth_headers'])
    tn.assert_success(response)
    app_types = response.json()['manifest']['types']
    schema = None
    for t in app_types:
        if t['name'] is schema_type:
            schema = t
            break
    return schema
    
def objectCopy(auth_headers, id, a, b):
    '''copy an object from one bucket to another'''
    url = config['api_url'] + '/iss/' + id + '/' + a + '?bucket=' + b
    response = requests.post(url, headers = auth_headers)
    tn.assert_success(response)
    return response.json()['id']

def deepObjectCopy(auth_headers, id, a, b):
    '''
    copy an object to a new bucket, as well as all of it's immutable references
    based on the object schema int the new realm
    '''
    new_object = objectCopy(auth_headers, id, a, b)
    get


config = authenticate(tn.read_config('config.json'))
print(str(getContext(config, 'dev-waugh')))
