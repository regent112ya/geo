# pip3 install flake8

import os, sys
import datetime

from subprocess import Popen, PIPE
from multiprocessing import Pool, cpu_count

def method(filepath):
	proc = Popen(
		'flake8 {} {}'.format(
			'--ignore=E116,E117,E201,E202,E203,E251,E261,E262,E265,E266,E301,E302,E305,E306,E402,E501,E722,E731,E741,W191,W504',
			filepath
		),
		shell = True,
		stdout = PIPE,
		stderr = PIPE
	)
	proc.wait()
	res = proc.communicate()
	str_res = res[0].decode('utf-8').strip()
	if str_res:
		print(str_res)
	else:
		print(f'{filepath} - [ok]')
	if proc.returncode:
		print(proc.returncode)
		print(res[1])

if __name__ == '__main__':
	res = [
		'geo_app/models.py',
		'geo_app/views.py',
		'geo/join.py',
		'csv_parser.py'
	]
	last_start = 0.0
	try:
		for _ in range(1):
			if not os.path.exists('code_validator.now'):
				break
			f = open('code_validator.now', 'r')
			value = f.readline()
			try:
				last_start = float(value.strip())
			except:
				pass
			f.close()
			if not last_start:
				break
			filestamps = [(el, os.path.getmtime(el) > last_start) for el in res]
			res = [el[0] for el in filestamps if el[1]]
	except Exception as err:
		print(err)
	Pool(cpu_count()).map(method, res)
	print('DONE')
	f = open('code_validator.now', 'w')
	f.write(str(datetime.datetime.now().timestamp()))
	f.close()
