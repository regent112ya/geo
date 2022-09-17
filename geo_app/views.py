# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from get.config import DADATA_TOKEN, DADATA_SECRET
from geo.join import initLog

import requests
import logging

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
