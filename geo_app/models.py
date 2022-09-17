# -*- coding: utf-8 -*-

from django.db import models

class Address(models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	address = models.TextField()
	postal_code = models.TextField()
	area = models.ForeignKey('Area', null=True, on_delete=models.SET_NULL)
	region = models.ForeignKey('Region', null=True, on_delete=models.SET_NULL)
	federal_district = models.ForeignKey('FederalDistrict', null=True, on_delete=models.SET_NULL)
	country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)
	city = models.ForeignKey('City', null=True, on_delete=models.SET_NULL)
	settlement = models.ForeignKey('Settlement', null=True, on_delete=models.SET_NULL)
	kladr_id = models.BigIntegerField()
	fias_id = models.TextField()
	fias_level = models.SmallIntegerField()
	capital_marker = models.SmallIntegerField()
	okato = models.TextField()
	oktmo = models.TextField()
	tax_office = models.TextField()
	tzint = models.SmallIntegerField()
	population = models.IntegerField()
	foundation_year = models.TextField()

class Area(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)
	geotype = models.ForeignKey('GeoType', null=True, on_delete=models.SET_NULL)

class Region(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)
	federal_district = models.ForeignKey('FederalDistrict', null=True, on_delete=models.SET_NULL)
	geotype = models.ForeignKey('GeoType', null=True, on_delete=models.SET_NULL)

class FederalDistrict(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)
	country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)

class Country(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)

class Settlement(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)
	geotype = models.ForeignKey('GeoType', null=True, on_delete=models.SET_NULL)

class City(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)
	geotype = models.ForeignKey('GeoType', null=True, on_delete=models.SET_NULL)

class GeoType(models.Model):
	name = models.TextField(unique=True)
