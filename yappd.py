# -*- coding: utf-8 -*-

import urllib2, urllib
import json


API_URL = 'https://pddimp.yandex.ru'

class YandexPPDApi(object):

	def __init__(self, api_token, domain):
		self.token = api_token
		self.domain = domain

		self.headers = { 'PddToken': self.token, }

	def check_error(self, response):
		res = json.loads( response.read())

		if res['success'] == 'error':
			print 'Ошибка: ', res
			return 1

		return 0


	def create_user(self, u_login, u_password):
		data = {
			'domain': self.domain,
			'login': u_login,
			'password': u_password,
		}

		try:
			req = urllib2.Request(API_URL + '/api2/admin/email/add', urllib.urlencode(data), self.headers)
			response = urllib2.urlopen(req)
		except urllib2.URLError as e:
			print "Ошибка при подключении"
			return 1
		return self.check_error(response)


	def edit_user_details(self, login, password = None, iname = None, fname = None, 
			enabled = None, sex = None, birth_date=None, hintq=None, hinta=None):
		data = {
			u'domain': self.domain,
			u'login': login,
		}
		if not password is None:
			data[u'password'] = password
		if not iname is None:
			data[u'iname'] = iname
		if not fname is None:
			data[u'fname'] = fname
		if not enabled is None:
			data[u'enabled'] = enabled
		if not sex is None:
			data[u'sex'] = sex
		if not birth_date is None:
			data[u'birth_date'] = birth_date
		if not hintq is None:
			data[u'hintq'] = hintq
		if not hinta is None:
			data[u'hinta'] = hinta
		if not enabled is None:
			data[u'enabled'] = enabled

		for k,v in data.iteritems():
			data[k] = unicode(v).encode('utf-8')

		try:
			req = urllib2.Request(API_URL + '/api2/admin/email/edit', urllib.urlencode(data), self.headers)
			response = urllib2.urlopen(req)
		except urllib2.URLError as e:
			print "Ошибка при подключении"
			return 1
		return self.check_error(response)

	def delete_user(self, login):
		data = {
			'domain': self.domain,
			'login': login,
		}

		try:
			req = urllib2.Request(API_URL + '/api2/admin/email/del', urllib.urlencode(data), self.headers)
			response = urllib2.urlopen(req)
		except urllib2.URLError as e:
			print "Ошибка при подключении"
			return 1
		return self.check_error(response)
