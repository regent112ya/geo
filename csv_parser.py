# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geo.settings")
import django
django.setup()

from geo_app.models import Address, Region, FederalDistrict, Country

if __name__ == '__main__':
	fields = 'address,postal_code,country,federal_district,region_type,region,area_type,area,city_type,city,settlement_type,settlement,kladr_id,fias_id,fias_level,capital_marker,okato,oktmo,tax_office,timezone,geo_lat,geo_lon,population,foundation_year'.split(',')
