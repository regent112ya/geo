# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from geo.config import DADATA_TOKEN, DADATA_SECRET
from geo.join import initLog
from geo_app.models import Address

import requests
import logging
import math

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

def get_dist(lat1, lng1, lat2, lng2):
	"""
	return distance <metrs>
	"""
	koef_rad = math.pi / 180.0
	latitude = lat1 * koef_rad
	sin_lat = math.sin(latitude)
	cos_lat = math.cos(latitude)
	longtitude = lng1 * koef_rad
	koef_dis = 20000 / math.pi
	if lat1 == lat2 and lng1 == lng2:
		return 0.0
	lat = lat2 * koef_rad
	lng = lng2 * koef_rad
	value = sin_lat * math.sin(lat) + cos_lat * math.cos(lat) * math.cos(lng - longtitude)
	if value > 1.0:
		value = 1.0
	elif value < -1.0:
		value = -1.0
	return math.acos(value) * koef_dis

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
	return (res[0]['geo_lat'], res[0]['geo_lon']) if res and res[0]['qc_geo'] < 5 else None

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

def index(http_request):
	return render(http_request, 'geo_app/index.html', {})

@ajax
def get_addrs(http_request):
	lat = float(http_request.POST['lat'])
	lng = float(http_request.POST['lng'])
	radius = int(http_request.POST['radius'])
	offset = radius / 111.3
	lat_range = (lat - offset, lat + offset)
	lng_range = (lng - offset, lng + offset)
	addrs = [el for el in list(
		Address.objects.filter(
			lat__range = lat_range,
			lng__range = lng_range
		).order_by('id').values_list(
			'id',
			'lat',
			'lng',
			'address'
		)[:200]
	) if get_dist(el[1], el[2], lat, lng) <= radius]
	return {
		'addrs': addrs
	}
