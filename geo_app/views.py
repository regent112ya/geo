# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from geo.settings import DEBUG, BASE_DIR
from get.config import DADATA_TOKEN, DADATA_SECRET

import requests

import os
import logging
import logging.handlers

def createFolders(basedir, path):
	folders = path.split('/')
	basedir = BASE_DIR + basedir
	while len(folders) > 0:
		basedir = basedir + '/' + folders[0]
		if not os.path.isdir(basedir):
			os.makedirs(basedir)
		del folders[0]

def initLog(filename=None):
	if filename is None:
		filename = 'geo_app_{}.log'.format(timezone.now().strftime('%Y%m%d%H%M%S'))
	createFolders('', 'logs')
	h = logging.handlers.RotatingFileHandler(
		filename = 'logs/{}'.format(filename),
		maxBytes = 200 * 1024 * 1024,
		backupCount = 20
	)
	h.setFormatter(logging.Formatter('%(asctime)s %(module)s:%(lineno)d %(levelname)s %(message)s'))
	LOG = logging.getLogger()
	LOG.addHandler(h)
	LOG.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
	return LOG

initLog()

def ajax(f):
	def wrapper(*args, **kwargs):
		try:
			res = f(*args, **kwargs)
		except Exception as err:
			logging.exception(err)
			res = {'fail': 'ERROR'}
		return JsonResponse(res)
	return wrapper

def _get_loc(address):
	headers = {
		'Content-Type': 'application/json',
		'Authorization': f'Token {DADATA_TOKEN}',
		'X-Secret': DADATA_SECRET,
	}
	link = 'https://cleaner.dadata.ru/api/v1/clean/address'
	resp = requests.post(
		link,
		json = [address],
		headers = headers,
		timeout = (20, 5)
	)
	if resp.status_code != 200:
		logging.error(resp.text)
		raise
	res = resp.json()
	return (res['geo_lat'][0], res['geo_lon'][0]) if res and res[0]['qc_geo'] < 5 else None

@ajax
def get_loc(http_request):
	address = http_request.POST.get('address')
	if not address:
		return {'fail': 'ADDRESS_NULL'}
	loc = _get_loc(address)
	if loc is None:
		return {'fail': 'ADDRESS_NOTFOUND'}
	return {
		'lat': loc[0],
		'lng': loc[1]
	}
