#!/usr/bin/env python

from bottle import route, run, request, response, abort, default_app, get, post
import json
from create import create
from delete import delete
from retrieve import retrieve
from add_activities import add_activities

import os
import re
import sys
import os.path

import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey,KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table


def createDynamoObject():
	try:
		users = Table.create('data', schema=[HashKey('id')],global_indexes=[GlobalAllIndex('EverythingIndex', parts=[HashKey('name')])],connection=boto.dynamodb2.connect_to_region('us-west-2'));
	except boto.exception.JSONResponseError:
		users = Table('data',connection=boto.dynamodb2.connect_to_region('us-west-2'))
		print "1) Table 'data' already created."
	#On first Run this wont insert data because of delay to create table on aws server side.
	try:
		users.put_item(data={
		'id': '3',
		'type': 'person',
		'name': 'dummy',
		'activities': ['activity one'],
		})
	except:
		print "2) Dummy Data already added."
	return users

boto = createDynamoObject()


@route('/create')
def parse_create():
	rq_id = request.query.id
	rq_name = request.query.name
	rq_activities = request.query.activities
	final_response= create.do_create(rq_id, rq_name, rq_activities, boto)
	response.set_header('Content-Language', 'en')
	response.status = final_response['status']
	json_response = final_response['json']
	json_ret = json.dumps(json_response)
	return json_ret

@route('/retrieve')
def parse_retrieve():
	rq_id = request.query.id
	rq_name = request.query.name
	rq_activities = request.query.activities
	final_response= retrieve.do_retrieve(rq_id, rq_name, rq_activities,boto)
	response.set_header('Content-Language', 'en')
	response.status = final_response['status']
	json_response = final_response['json']
	json_ret = json.dumps(json_response)
	return json_ret

@route('/delete')
def parse_delete():
	rq_id = request.query.id
	rq_name = request.query.name
	rq_activities = request.query.activities
	final_response= delete.do_delete(rq_id, rq_name, rq_activities)
	response.set_header('Content-Language', 'en')
	response.status = final_response['status']
	json_response = final_response['json']
	json_ret = json.dumps(json_response)
	return json_ret

@route('/add_activities')
def parse_add_activities():
	rq_id = request.query.id
	rq_activities = request.query.activities
	final_response= add_activities.do_add_activities(rq_id, rq_activities, boto)
	response.status = final_response['status']
	json_response = final_response['json']
	json_ret = json.dumps(json_response)
	return json_ret

run(host='localhost', port=8080, debug=True)