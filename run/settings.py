#!/usr/bin/env python3.7
# coding=utf-8
from decrypt import Decrypt

# Flask settings
# localhost:5000 -> 0.0.0.0:5000
FLASK_SERVER_NAME = 'localhost:5000'

FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
DB_RESET = True
USERNAME = 'masteruser'
PASSWORD = Decrypt().decrypt_file(file_name='./database/db.enc')
HOST = 'tms.c08i2kco4yjx.us-east-1.rds.amazonaws.com'
PORT = 5432
DATABASE = 'tms'

SQLALCHEMY_DATABASE_URI = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
