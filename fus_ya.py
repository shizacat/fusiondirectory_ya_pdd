#!/usr/bin/python
# -*- coding: utf-8 -*-

# https://github.com/V-Alexeev/yandexmailapi
#
# user postmodify /script/fus_ya.py -t modify -l %uid% -n '%givenName%' -s '%sn%' -p '%gender%' -b '%dateOfBirth%'
# user postremove /script/fus_ya.py -t delete -l %uid%
# user postcreate /script/fus_ya.py -t create -l %uid% -n '%givenName%' -s '%sn%' -p '%gender%' -b '%dateOfBirth%'
#
# Отдельно для пароля (Password Hook)
# /script/fus_ya.py -t password


"""yandex_domain

Usage:
	test.py -t (modify | create | delete ) -l <login> [-n <iname>] [-s <fname>] [-p <sex>] [-b <birth_date>] [-hq <hintq>] [-ha <hinta>]
	test.py -t password [INPUT ...]

Options:
"""
from docopt import docopt
from yappd import YandexPPDApi

import random
import string
import os


arguments = docopt(__doc__, version='Yandex domain Fusiondirectory 1.0')
# print(arguments)

# Получаем настройки
try:
	conf_file = os.path.join( os.path.abspath(os.path.dirname(__file__)), 'config')
	f = open(conf_file, 'r')
	l =  f.readlines()
	if len(l) < 2:
		print "Неверный файл настроек"
		exit(1)
	api_token = l[0].strip()
	domain = l[1].strip()
	f.close()
except (OSError, IOError) as e:
	print e
	exit(1)

def random_str(x):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(x))

def data_mod_user():
	arg = {
		'login': arguments['<login>']
	}
	if arguments['-n']:
		arg['iname'] = arguments['<iname>'].decode('utf-8')
	if arguments['-s']:
		arg['fname'] = arguments['<fname>'].decode('utf-8')
	if arguments['-p']:
		if arguments['<sex>'] == 'M':
			arg['sex'] = '1'
		elif arguments['<sex>'] == 'F':
			arg['sex'] = '2'
		else:
			arg['sex'] = '0'
	if arguments['-b']:
		lb = arguments['<birth_date>'].split('.')
		arg['birth_date'] = '-'.join([lb[2], lb[1], lb[0]])
	
	arg['hintq'] = random_str(20)
	arg['hinta'] = random_str(19)

	return arg


if arguments['create']:
	login = arguments['<login>']
	password = random_str(10)

	ppd = YandexPPDApi(api_token, domain)
	code = ppd.create_user(login, password)

	if code == 0:
		arg = data_mod_user()
		code = ppd.edit_user_details( **arg)

	exit(code)


if arguments['modify']:
	arg = data_mod_user()
	ppd = YandexPPDApi(api_token, domain)
	code = ppd.edit_user_details( **arg)
	
	exit(code)


if arguments['delete']:
	login = arguments['<login>']

	ppd = YandexPPDApi(api_token, domain)
	code = ppd.delete_user(login)
	exit(code)

if arguments['password']:
	if len( arguments['INPUT']) >= 2:
		login = arguments['INPUT'][0]
		password = arguments['INPUT'][1]

		ppd = YandexPPDApi(api_token, domain)
		code = ppd.edit_user_details(login= login, password= password)
		exit(code)


