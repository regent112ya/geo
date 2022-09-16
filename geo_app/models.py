# -*- coding: utf-8 -*-

from django.db import models

class Address(models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	address = models.TextField()
	postal_code = models.TextField()
	area = models.ForeignKey('Area', null=True, on_delete=models.SET_NULL)
	region = models.ForeignKey('Region', null=True, on_delete=models.SET_NULL)
	city = models.ForeignKey('City', null=True, on_delete=models.SET_NULL)
	settlement = models.ForeignKey('Settlement', null=True, on_delete=models.SET_NULL)
	kladr_id = models.IntegerField()
	fias_id = models.TextField()
	fias_level = models.SmallIntegerField()
	capital_marker = models.SmallIntegerField()
	okato = models.IntegerField(null=True)
	oktmo = models.IntegerField(null=True)
	tax_office = models.IntegerField(null=True)
	tzint = models.SmallIntegerField(default=0)
	population = models.IntegerField()
	foundation_year = models.TextField()

class Area(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)
	atype = models.ForeignKey('AreaType', null=True, on_delete=models.SET_NULL)

class AreaType(models.Model):
	name = models.TextField(unique=True)

class Region(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)
	federal_district = models.ForeignKey('FederalDistrict', null=True, on_delete=models.SET_NULL)
	rtype = models.ForeignKey('RegionType', null=True, on_delete=models.SET_NULL)

class RegionType(models.Model):
	name = models.TextField(unique=True)

class FederalDistrict(models.Model):
	name = models.TextField()
	lowername = models.TextField(unique=True)
	country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)

class Country(models.Model):
	name = models.TextField()

