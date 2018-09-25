# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     11/16/2015
# Modified: 
# Desc:     Worker for general RKS functions

import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import decimal_logging as dl
import json

# Return the RKS entry
#   param iam: connection settings (url and unique basic user authentication)
#   param rks_id: RKS entry id
def get_rks_entry(iam, rks_id, rks_record_app = 'planning'):
    dl.debug("get_rks_entry")
    url = "/rks/" + rks_id + "?context=" + iam["apps"][rks_record_app]["context_id"]
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
def find_entry(iam, record, name, parent = None, rks_record_app = 'planning'):
    dl.debug("find_entry")
    url = "/rks?context=" + iam["apps"][rks_record_app]["context_id"] + \
        "&record=" + iam["account_name"] + "/" + rks_record_app + "/" + record + "&name=" + name
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
#   param content: search record body
#   returns: matching entry if one exists, or None otherwise
def search_for_record_entries(iam, content):
    dl.debug("search_for_record_entries")
    print(content)
    url = "/rks/search?context=" + iam["apps"]["planning"]["context_id"]
    entries = thinknode.post(iam, url, content)
    print(entries)
    if len(entries) != 0:
        return entries
    else:
        return None

# Check if an entry exists in the planning RKS inactive records
#   param iam: connection settings (url and unique basic user authentication)
#   param record: RKS record type
#   param name: unique RKS record name
#   param parent: RKS parent
#   returns: matching entry if one exists, or None otherwise
def find_entry_inactive(iam, record, name, parent = None, rks_record_app = 'planning'):
    dl.debug("find_entry_inactive")
    url = "/rks?context=" + iam["apps"][rks_record_app]["context_id"] + \
        "&record=" + iam["account_name"] + "/" + rks_record_app + "/" + record + "&name=" + name + "&inactive=true"
    if (parent):
        url += "&parent=" + parent
    entries = thinknode.get(iam, url)
    if len(entries) != 0:
        return entries[0]
    else:
        return None

def find_entry_by_record_type(iam, record, parent = None, rks_record_app = 'planning'):
    url = "/rks?context=" + iam["apps"][rks_record_app]["context_id"] + \
        "&record=" + iam["account_name"] + "/" + rks_record_app + "/" + record + "&inactive=false&recursive=true"
    if (parent):
        url += "&parent=" + parent
    entries = thinknode.get(iam, url)
    if len(entries) != 0:
        return entries
    else:
        return None

def find_inactive_entry_by_record_type(iam, record, parent = None, rks_record_app = 'planning'):
    url = "/rks?context=" + iam["apps"][rks_record_app]["context_id"] + \
        "&record=" + iam["account_name"] + "/" + rks_record_app + "/" + record + "&inactive=true"
    if (parent):
        url += "&parent=" + parent
    entries = json.loads(thinknode.get(iam, url))
    if len(entries) != 0:
        return entries
    else:
        return None

def get_rks_entry_children(iam, record_id, rks_record_app = 'planning', recursive = 'true', record = None):
    dl.debug("get_rks_entry_children")
    url = "/rks?context=" + iam["apps"][rks_record_app]["context_id"] + "&parent=" + record_id + '&recursive=' + recursive
    if (record):
        url += '&record=' + iam["account_name"] + "/" + rks_record_app + "/" + record
    
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
        dl.error('Deleting record ' + record_id + ' failed' + res)
    else:
        dl.debug('Deleting record ' + record_id + ' successful')


def mark_rks_entry_active(iam, record, name, parent = None, rks_record_app = 'planning'):
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
        thinknode.put(iam, "/rks/" + entry["id"] + "?context=" + iam["apps"][rks_record_app]["context_id"],
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
def write_rks_entry(iam, record, iss_type, name, data, parent = None, data_app_name = 'dosimetry', rks_record_app = 'planning'):
    dl.debug("write_rks_entry")
    print(str(data))
    # Post to ISS
    scope = thinknode.make_named_type_scope(iam, data_app_name, iss_type)
    res = thinknode.post_immutable(iam, data_app_name, data, scope, False)
    iss_id = json.loads(res.text)["id"]

    entry = find_entry(iam, record, name, parent, rks_record_app)
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
        thinknode.put(iam, "/rks/" + entry["id"] + "?context=" + iam["apps"][rks_record_app]["context_id"],
            json.dumps(updated_entry))
        return entry["id"]
    # Otherwise, create it.
    else:
        # Check for archived result first
        a_entry = find_entry_inactive(iam, record, name, parent, rks_record_app)
        if a_entry:
            mark_rks_entry_active(iam, record, name, parent, rks_record_app)
            updated_entry = {
                "name": name,
                "immutable": iss_id,
                "active": True,
                "revision": a_entry["revision"]
            }
            if (parent):
                updated_entry["parent"] = parent
            thinknode.put(iam, "/rks/" + a_entry["id"] + "?context=" + iam["apps"][rks_record_app]["context_id"],
                json.dumps(updated_entry))
            return a_entry["id"]
        else:
            new_entry = {
                "name": name,
                "immutable": iss_id,
                "active": True
            }
            if (parent):
                new_entry["parent"] = parent
            scope = '/rks/' + iam["account_name"] + '/' + rks_record_app + '/' + record
            res = thinknode.post_immutable(iam, rks_record_app, new_entry, scope, False)
            return json.loads(res.text)["id"]

# Lock an RKS entry
#   param iam: conection settings (url and unique basic user authentication)
#   param rks_id: The RKS entry id
#   param revision_id: The RKS entry revision id
#   param app: The app name the RKS entry belongs to
#   param deep: Whether to perform a shallow or deep lock. Defaults to shallow.
def lock_rks_entry(iam, rks_id, revision_id, app, deep = 'false'):
    dl.debug("lock_rks_entry")

    dl.debug(iam["apps"][app]["context_id"])
    revision = \
        {
            "revision": revision_id
        }
    thinknode.put(iam, "/rks/" + rks_id + "/lock?context=" + iam["apps"][app]["context_id"] + 
        "&deep=" + deep, json.dumps(revision))

# Unlock an RKS entry
#   param iam: conection settings (url and unique basic user authentication)
#   param rks_id: The RKS entry id
#   param revision_id: The RKS entry record as a dictionary
#   param app: The app name the RKS entry belongs to
#   param deep: Whether to perform a shallow or deep lock. Defaults to shallow.
def unlock_rks_entry(iam, rks_id, revision_id, app, deep = 'false'):
    dl.debug("unlock_rks_entry")

    dl.debug(iam["apps"][app]["context_id"])
    revision = \
        {
            "revision": revision_id
        }
    thinknode.put(iam, "/rks/" + rks_id + "/unlock?context=" + iam["apps"][app]["context_id"] + 
        "&deep=" + deep, json.dumps(revision))