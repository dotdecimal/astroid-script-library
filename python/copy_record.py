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

def getBucket(config, realm):
    '''returns the bucket of a given realm'''
    url = config['api_url'] + '/iam/realms/' + realm
    response = requests.get(url, headers = config['auth_headers'])
    tn.assert_success(response)
    return response.json()['bucket']

def getContext(config, realm):
    '''returns the context of a given realm'''
    url = config['api_url'] + '/iam/realms/' + realm + '/context'
    response = requests.get(url, headers = config['auth_headers'])
    tn.assert_success(response)
    return response.json()['id']

def getObject(config, id, context):
    '''returns an object from a given context'''
    url = config['api_url'] + '/iss/' + id + '?context=' + context
    response = requests.get(url, headers = config['auth_headers'])
    tn.assert_success(response)
    return response.json()


def getObjectType(config, context, id):
    url = config['api_url'] + '/iss/' + id + '/' + context
    response = requests.head(url, headers = config['auth_headers'])
    tn.assert_success(response)
    result = response.json()['type']
    return result

def getObjectVersion(config, type, realm):
    app = '/'.split(type)[2]
    url = config['api_url'] + '/apm/apps/' + config['account'] + '/' + app + '/versions'
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
    return schema['schema']
    
def objectCopy(config, id, a, b):
    '''copy an object from one bucket to another'''
    url = config['api_url'] + '/iss/' + id + '/' + a + '?bucket=' + b
    response = requests.post(url, headers = config['auth_headers'])
    tn.assert_success(response)
    return response.json()['id']

def deepObjectCopyRecurse(config, object, schema, a, b):
    '''Search through an object's children for other objects that must be copied'''
    for key, value in object_schema.items():
        switch(key):
            case 'dynamic_type':
            case 'array_type':
            case 'structure_type':
            case 'map_type':
            case 'union_type':
            case 'reference_type':
            case 'named_type':
            case 'optional':


def deepObjectCopy(config, id, a, b):
    '''
    copy from one realm to another, as well as all of it's immutable references
    based on the object schema int the new realm

    @param a: the realm the id is copied from
    @param b: the realm the id is copied to
    '''
    bucket_a = getBucket(config, a)
    bucket_b = getBucket(config, b)
    context_b = getContext(config, b)
    new_object_id = objectCopy(config['auth_headers'], id, bucket_a, bucket_b)
    new_object = getObject(config['auth_headers', ])
    object_type = getObjectType(config, context_b, new_object_id)
    object_version = getObjectVersion(config, object_type, b)
    object_schema = getSchema(config, object_type, object_version)
    deepObjectCopyRecurse()

    return new_object_id
    



config = authenticate(tn.read_config('config.json'))
print(str(getContext(config, 'dev-waugh')))
