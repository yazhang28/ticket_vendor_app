#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" configuration run file of our api """
import logging.config
from flask import Flask, Blueprint
from api.ticket.endpoints.buyer import ns as ticket_buyer_namespace
from api.ticket.endpoints.buyer_referral_type import ns as ticket_buyer_referral_type_namespace
from api.ticket.endpoints.city import ns as ticket_city_namespace
from api.ticket.endpoints.event import ns as ticket_event_namespace
from api.ticket.endpoints.payment_method import ns as ticket_payment_method_namespace
from api.ticket.endpoints.ticket import ns as ticket_ticket_namespace
from api.config import api
from database import db, reset_database
import settings

app = Flask(__name__)

# logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
# logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):

    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app):
    """ Initialize app and flask configuration """
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    api.add_namespace(ticket_buyer_namespace)
    api.add_namespace(ticket_buyer_referral_type_namespace)
    api.add_namespace(ticket_city_namespace)
    api.add_namespace(ticket_event_namespace)
    api.add_namespace(ticket_payment_method_namespace)
    api.add_namespace(ticket_ticket_namespace)

    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)
    reset_database()

def main():
    initialize_app(app)
    log.info('Starting app...')
    api.run(debug=True)

if __name__ == '__main__':
    main()

