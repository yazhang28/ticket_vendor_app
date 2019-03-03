# coding=utf-8
#!/usr/bin/env python3
from decrypt import Decrypt

# Flask settings
FLASK_SERVER_NAME = 'localhost:5000'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
USERNAME = 'masteruser'
PASSWORD = Decrypt().decrypt_file(file_name='./database/db.enc')
HOST = 'tms.c08i2kco4yjx.us-east-1.rds.amazonaws.com'
PORT = 5432
DATABASE = 'tms'

SQLALCHEMY_DATABASE_URI = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
