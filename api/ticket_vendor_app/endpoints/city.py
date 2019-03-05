#!/usr/bin/env python3
# coding=utf-8

""" City API Endpoints """
import logging
from flask import request
from flask_restplus import Resource, fields
from api.config import api
from api.ticket_vendor_app.endpoints.parsers import CityParser
from api.ticket_vendor_app.business_domain import CityDomain
from database.models import City

log = logging.getLogger(__name__)
ns = api.namespace('ticket-vendor/city', description='Operations related to City entity')
city_domain = CityDomain()

post_payload = api.model('city', {
    'id': fields.Integer(readOnly=True, description="Unique identifier of a City"),
    'name': fields.String(required=True, max_length=50, description='vendor referral source used by City')
})

@ns.route('/')
@api.response(400, "Bad Request")
class CityCollection(Resource):
    """ End points ticket-vendor/City """

    @api.marshal_list_with(post_payload)
    def get(self):
        """ Returns list of all event cities """

        city = City.query.all()
        return city

    @api.response(201, "City created")
    @api.expect(post_payload)
    @api.marshal_with(post_payload)
    def post(self):
        """ Creates new event city """

        parsed_args = CityParser.args.parse_args(request)
        city = city_domain.create_city(parsed_args)
        if city:
            return city
        api.abort(404)

@ns.route('/<int:id>')
@api.response(200, 'Request Successful')
@api.response(404, 'Bad Request')
class CityItem(Resource):
    """ End points for ticket-vendor/city/id """

    @api.marshal_with(post_payload)
    def get(self, id):
        """ Return event city by id """
        return city_domain.get_city(id)

