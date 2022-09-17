# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geo.settings")
import django
django.setup()
from django.db import transaction

from geo_app.models import (
	Address,
	Area,
	City,
	Country,
	FederalDistrict,
	GeoType,
	Region,
	Settlement
)
from geo.join import initLog

import csv
import logging
import re

if __name__ == '__main__':
	initLog(filename='csv_parser.log')
	fields = 'address,postal_code,country,federal_district,region_type,region,area_type,area,city_type,city,settlement_type,settlement,kladr_id,fias_id,fias_level,capital_marker,okato,oktmo,tax_office,timezone,geo_lat,geo_lon,population,foundation_year'.split(',')
	d_fields = {}
	def get_val(line, name):
		index = d_fields.get(name)
		if index is None or index >= len(line):
			return ''
		return line[index]
	def get_geotype(*args):
		geo_type = get_val(*args)
		geotype_obj = None
		if geo_type:
			geotype_obj, _ = GeoType.objects.get_or_create(name = geo_type)
		return geotype_obj
	count_passed = 0
	count_failed = 0
	with open('city.csv') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		is_firstline = True
		for line in reader:
			try:
				if not line:
					continue
				if is_firstline:
					for index, name in enumerate(line):
						d_fields[name.strip()] = index
					is_firstline = False
					continue
				address = get_val(line, 'address')
				lat, lng = get_val(line, 'geo_lat'), get_val(line, 'geo_lon')
				if not address or not lat or not lng:
					continue
				lat = float(lat)
				lng = float(lng)
				with transaction.atomic():
					# creating settlement
					settlement = get_val(line, 'settlement')
					settlement_obj = None
					if settlement:
						geotype_obj = get_geotype(line, 'settlement_type')
						lowername = settlement.lower()
						settlement_obj = Settlement.objects.filter(
							lowername__exact = lowername
						).only('id').first()
						if settlement_obj is None:
							settlement_obj = Settlement.objects.create(
								name = settlement,
								lowername = lowername,
								geotype = geotype_obj
							)
					#
					# creating area
					area = get_val(line, 'area')
					area_obj = None
					if area:
						geotype_obj = get_geotype(line, 'area_type')
						lowername = area.lower()
						area_obj = Area.objects.filter(
							lowername__exact = lowername
						).only('id').first()
						if area_obj is None:
							area_obj = Area.objects.create(
								name = area,
								lowername = lowername,
								geotype = geotype_obj
							)
					#
					# creating city
					city = get_val(line, 'city')
					city_obj = None
					if city:
						geotype_obj = get_geotype(line, 'city_type')
						lowername = city.lower()
						city_obj = City.objects.filter(
							lowername__exact = lowername
						).only('id').first()
						if city_obj is None:
							city_obj = City.objects.create(
								name = city,
								lowername = lowername,
								geotype = geotype_obj
							)
					#
					# creating Country
					country = get_val(line, 'country')
					country_obj = None
					if country:
						lowername = country.lower()
						country_obj = Country.objects.filter(
							lowername__exact = lowername
						).only('id').first()
						if country_obj is None:
							country_obj = Country.objects.create(
								name = country,
								lowername = lowername
							)
					#
					# creating FederalDistrict
					federal_district = get_val(line, 'federal_district')
					fd_obj = None
					if federal_district:
						lowername = federal_district.lower()
						fd_obj = FederalDistrict.objects.filter(
							lowername__exact = lowername
						).only('id').first()
						if fd_obj is None:
							fd_obj = FederalDistrict.objects.create(
								name = federal_district,
								lowername = lowername,
								country = country_obj
							)
					#
					# creating Region
					region = get_val(line, 'region')
					region_obj = None
					if region:
						geotype_obj = get_geotype(line, 'region_type')
						lowername = region.lower()
						region_obj = Region.objects.filter(
							lowername__exact = lowername
						).only('id').first()
						if region_obj is None:
							region_obj = Region.objects.create(
								name = region,
								lowername = lowername,
								geotype = geotype_obj
							)
					#
					# creating Address
					postal_code = get_val(line, 'postal_code')
					kladr_id = int(get_val(line, 'kladr_id'))
					fias_id = get_val(line, 'fias_id')
					fias_level = int(get_val(line, 'fias_level'))
					capital_marker = int(get_val(line, 'capital_marker'))
					okato = get_val(line, 'okato')
					oktmo = get_val(line, 'oktmo')
					tax_office = get_val(line, 'tax_office')
					tzint = get_val(line, 'timezone')
					if tzint:
						tzint = int(tzint[tzint.rindex('UTC') + 3 : ])
					else:
						tzint = 0
					population = get_val(line, 'population')
					population = int(re.finditer('[0-9]+', population).__next__().group())
					foundation_year = get_val(line, 'foundation_year')
					Address.objects.create(
						address = address,
						lat = lat,
						lng = lng,
						postal_code = postal_code,
						area = area_obj,
						region = region_obj,
						federal_district = fd_obj,
						country = country_obj,
						city = city_obj,
						settlement = settlement_obj,
						kladr_id = kladr_id,
						fias_id = fias_id,
						fias_level = fias_level,
						capital_marker = capital_marker,
						okato = okato,
						oktmo = oktmo,
						tax_office = tax_office,
						tzint = tzint,
						population = population,
						foundation_year = foundation_year
					)
					#
					count_passed += 1
			except Exception as err:
				logging.error(line)
				logging.exception(err)
				count_failed += 1
	print(f'passed: {count_passed}\nfailed: {count_failed}\nLog: logs/csv_parser.log')
