#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" configuration run file of our api """

from flask import Flask, Blueprint
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)

def initialize_app(flask_app):
    """ Initialize app and flask configuration """
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint, title='Ticket Vendor API')
    api.add_namespace(ticket_buyer_namespace)
    api.add_namespace(ticket_buyer_referral_type_namespace)
    api.add_namespace(ticket_city_type_namespace)
    api.add_namespace(ticket_event_namespace)
    api.add_namespace(ticket_payment_method_name)
    api.add_namespace(ticket_ticket_namespace)
    flask_app.register_blueprint(blueprint)
