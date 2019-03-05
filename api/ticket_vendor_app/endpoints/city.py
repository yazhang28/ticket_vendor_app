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
ns = api.namespace('ticket_vendor_app/city', description='Operations related to city entity')
city_domain = CityDomain()

post_payload = api.model('city', {
    'id': fields.Integer(readOnly=True, description="Unique identifier of a city"),
    'name': fields.String(required=True, description='vendor referral source used by city')
})

@ns.route('/')
@api.response(404, "Bad Request")
class CityCollection(Resource):
    """ End points ticket_vendor_app/city """

    @api.marshal_list_with(post_payload)
    def get(self):
        """ Returns list of referral types """

        city = City.query.all()
        return city

    @api.response(201, "city created")
    @api.expect(post_payload)
    @api.marshal_with(post_payload)
    def post(self):
        """ Creates new city """

        parsed_args = CityParser.args.parse_args(request)
        city = city_domain.create_city(parsed_args)
        if city:
            return city, 201
        api.abort(404)

@ns.route('/<int:id>')
@api.response(200, 'Request Successful')
@api.response(404, 'Bad Request')
class CityItem(Resource):
    """ End points for ticket_vendor_app/buyer/id """

    @api.marshal_with(post_payload)
    def get(self, id):
        """ Return city by Id """
        return city_domain.get_city(id), 200

