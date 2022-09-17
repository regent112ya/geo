# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

from geo.settings import DEBUG, BASE_DIR
from django.utils import timezone

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
	logpath = f'{BASE_DIR}/logs/{filename}'
	if os.path.exists(logpath):
		os.remove(logpath)
	h = logging.handlers.RotatingFileHandler(
		filename = logpath,
		maxBytes = 200 * 1024 * 1024,
		backupCount = 20
	)
	h.setFormatter(logging.Formatter('%(asctime)s %(module)s:%(lineno)d %(levelname)s %(message)s'))
	LOG = logging.getLogger()
	LOG.addHandler(h)
	LOG.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
	return LOG
