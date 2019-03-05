#!/usr/bin/env python3
# coding=utf-8

""" event API Endpoints """
import logging
from flask import request
from flask_restplus import Resource, fields
from api.config import api
from api.ticket_vendor_app.business_domain import EventDomain
from api.ticket_vendor_app.endpoints.parsers import EventParser
from database.models import Event
from database import db

ns = api.namespace('ticket_vendor_app/event', description='Operations related to ticket_vendor_app event entity')

post_payload = None

@ns.route('/')
@api.response(400, "Bad Request")
class EventCollection(Resource):
    """ End points ticket_vendor_app/event """

    @api.marshal_with_list(post_payload)
    def get(self):

        """ Returns list of all Events """
        event = Event.query.all()
        return event

    @api.response(200, "Request Successful")
    @api.expect(post_payload)
    def post(self):
        parsed_args = EventParser.parse()


