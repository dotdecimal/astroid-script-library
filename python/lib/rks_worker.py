# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     11/16/2015
# Modified: 
# Desc:     Worker for general RKS functions

import os.path
import sys
from lib import thinknode_worker as thinknode
from lib import decimal_logging as dl
import json

# Return the RKS entry
#   param iam: connection settings (url and unique basic user authentication)
#   param rks_id: RKS entry id
def get_rks_entry(iam, rks_id):
    dl.debug("get_rks_entry")
    url = "/rks/" + rks_id + "?context=" + iam["apps"]["planning"]["context_id"]
    entry = thinknode.get(iam, url)
    if entry != None:
        return entry
    else:
        dl.error("Unable to get rks entry with id: " + rks_id)
        sys.exit()

# Check if an entry exists in the planning RKS
#   param iam: connection settings (url and unique basic user authentication)
#   param record: RKS record type
#   param name: unique RKS record name
#   param parent: RKS parent
#   returns: matching entry if one exists, or None otherwise
def find_entry(iam, record, name, parent = None):
    dl.debug("find_entry")
    url = "/rks?context=" + iam["apps"]["planning"]["context_id"] + \
        "&record=" + iam["account_name"] + "/planning/" + record + "&name=" + name
    if (parent):
        url += "&parent=" + parent
    entries = thinknode.get(iam, url)
    if len(entries) != 0:
        return entries[0]
    else:
        return None

# Check if an entry exists in the planning RKS inactive records
#   param iam: connection settings (url and unique basic user authentication)
#   param record: RKS record type
#   param name: unique RKS record name
#   param parent: RKS parent
#   returns: matching entry if one exists, or None otherwise
def find_entry_inactive(iam, record, name, parent = None):
    dl.debug("find_entry_inactive")
    url = "/rks?context=" + iam["apps"]["planning"]["context_id"] + \
        "&record=" + iam["account_name"] + "/planning/" + record + "&name=" + name + "&inactive=true"
    if (parent):
        url += "&parent=" + parent
    entries = thinknode.get(iam, url)
    if len(entries) != 0:
        return entries[0]
    else:
        return None

def find_entry_by_record_type(iam, record, parent = None):
    url = "/rks?context=" + iam["apps"]["planning"]["context_id"] + \
        "&record=" + iam["account_name"] + "/planning/" + record + "&inactive=false&recursive=true"
    if (parent):
        url += "&parent=" + parent
    entries = thinknode.get(iam, url)
    if len(entries) != 0:
        return entries
    else:
        return None

def find_inactive_entry_by_record_type(iam, record, parent = None):
    url = "/rks?context=" + iam["apps"]["planning"]["context_id"] + \
        "&record=" + iam["account_name"] + "/planning/" + record + "&inactive=true"
    if (parent):
        url += "&parent=" + parent
    entries = json.loads(thinknode.get(iam, url))
    if len(entries) != 0:
        return entries
    else:
        return None

def get_rks_entry_children(iam, record_id):
    dl.debug("get_rks_entry_children")
    url = "/rks?context=" + iam["apps"]["planning"]["context_id"] + "&parent=" + record_id + '&recursive=true'
    
    entries = thinknode.get(iam, url)
    return entries

def get_rks_entry_history(iam, record_id):
    dl.debug("get_rks_entry_history")
    url = "/rks/" + record_id + "/history?context=" + iam["apps"]["planning"]["context_id"] 
    
    entries = thinknode.get(iam, url)
    return entries

def mark_rks_entry_inactive(iam, record, name, parent = None):
    entry = find_entry(iam, record, name, parent)
    if entry:
        updated_entry = {
            "name": "zzzzzzzzzz" + entry['name'],
            "immutable": entry["immutable"],
            "active": False,
            "revision": entry["revision"]
        }
        if (parent):
            updated_entry["parent"] = parent
        thinknode.put(iam, "/rks/" + entry["id"] + "?context=" + iam["apps"]["planning"]["context_id"],
            updated_entry)
        return entry["id"]

def delete_rks_entry(iam, record_id):
    dl.debug('Deleting rks record: ' + record_id)
    url = "/rks/" + record_id + "?context=" + iam["apps"]["planning"]["context_id"] + "&recursive=true"
    print(url)
    res = thinknode.delete(iam, url)
    if str(res) != '200':
        dl.error('Deleting record ' + record_id + ' failed')
    else:
        dl.debug('Deleting record ' + record_id + ' failed')


def mark_rks_entry_active(iam, record, name, parent = None):
    entry = find_entry(iam, record, name, parent)
    if entry:
        updated_entry = {
            "name": entry['name'],
            "immutable": entry["immutable"],
            "active": True,
            "revision": entry["revision"]
        }
        if (parent):
            updated_entry["parent"] = parent
        thinknode.put(iam, "/rks/" + entry["id"] + "?context=" + iam["apps"]["planning"]["context_id"],
            updated_entry)
        return entry["id"]

# Check if an entry exists in the planning RKS
#   param iam: connection settings (url and unique basic user authentication)
#   param record: RKS record type
#   param type: ISS type to post data to ISS as
#   param name: unique RKS record name
#   param data: data to post to ISS
#   param parent: RKS parent
#   returns: RKS ID
def write_rks_entry(iam, record, iss_type, name, data, parent = None, data_app_name = 'dosimetry'):
    dl.debug("write_rks_entry")
    print(str(data))
    # Post to ISS
    scope = thinknode.make_named_type_scope(iam, data_app_name, iss_type)
    res = thinknode.post_immutable(iam, data_app_name, data, scope, False)
    iss_id = json.loads(res.text)["id"]

    entry = find_entry(iam, record, name, parent)
    # If the entry exists, update it.
    if entry:
        updated_entry = {
            "name": name,
            "immutable": iss_id,
            "active": True,
            "revision": entry["revision"]
        }
        if (parent):
            updated_entry["parent"] = parent
        thinknode.put(iam, "/rks/" + entry["id"] + "?context=" + iam["apps"]["planning"]["context_id"],
            json.dumps(updated_entry))
        return entry["id"]
    # Otherwise, create it.
    else:
        # Check for archived result first
        a_entry = find_entry_inactive(iam, record, name, parent)
        if a_entry:
            mark_rks_entry_active(iam, record, name, parent)
            updated_entry = {
                "name": name,
                "immutable": iss_id,
                "active": True,
                "revision": a_entry["revision"]
            }
            if (parent):
                updated_entry["parent"] = parent
            thinknode.put(iam, "/rks/" + a_entry["id"] + "?context=" + iam["apps"]["planning"]["context_id"],
                json.dumps(updated_entry))
            return a_entry["id"]
        else:
            new_entry = {
                "name": name,
                "immutable": iss_id,
                "active": True
            }
            scope = '/rks/' + iam["account_name"] + '/planning' + '/' + record
            res = thinknode.post_immutable(iam, "planning", new_entry, scope, False)
            return res.text