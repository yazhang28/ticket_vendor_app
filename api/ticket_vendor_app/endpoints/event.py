#!/usr/bin/env python3.7
# coding=utf-8

""" Event API Endpoints """
import logging
from flask import request
from flask_restplus import Resource, fields
from api.config import api
from api.ticket_vendor_app.business_domain import EventDomain
from api.ticket_vendor_app.endpoints.parsers import EventParser
from api.ticket_vendor_app.endpoints.serializers import EventSerializer
from database.models import Event

log = logging.getLogger(__name__)
event_domain = EventDomain()
ns = api.namespace('ticket-vendor/event', description='Operations related to ticket_vendor_app Event entity')

@ns.route('/')
@api.response(400, "Bad Request")
class EventCollection(Resource):
    """ End points ticket-vendor/event """

    @api.marshal_list_with(EventSerializer.payload)
    def get(self):
        """ Returns list of all events """

        event = Event.query.all()
        return event

    @api.response(201, "Request Successful")
    @api.expect(EventSerializer.post_payload)
    @api.marshal_with(EventSerializer.payload)
    def post(self):
        """ Create new event """

        log.debug(request)
        parsed_args = EventParser.post_args.parse_args(request)
        event = event_domain.create_event(parsed_args)
        if event:
            return event
        elif event is None:
            api.abort(400, message='event already exists in the database')

@ns.route('/<string:city_txt>/<int:month_interval>')
@api.response(404, 'Not Found')
@api.response(200, 'Request Successful')
class EventItem(Resource):
    """ End points for ticket-vendor/buyer/id """

    @api.marshal_list_with(EventSerializer.payload)
    def get(self, city_txt, month_interval):
        """ Return events by city and month interval """

        events = event_domain.get_event_batch(city_txt, month_interval)
        log.debug(f'SELECT events by city :: {city_txt} :: between now and {month_interval} month(s) :: {repr(events)}')
        return events

