#!/usr/bin/env python3.7
# coding=utf-8

""" Buyer Endpoints """
import logging
from flask import request
from flask_restplus import Resource
from api.config import api
from api.ticket_vendor_app.business_domain import BuyerDomain
from api.ticket_vendor_app.endpoints.parsers import BuyerParser
from api.ticket_vendor_app.endpoints.serializers import BuyerSerializer
from database.models import Buyer

log = logging.getLogger(__name__)
ns = api.namespace('ticket-vendor/buyer', description='Operations related to ticket_vendor_app: Buyer entity')

@ns.route('/')
@api.response(400, "Bad Request")
class BuyerCollection(Resource):
    """ End points ticket-vendor/buyer """

    @api.marshal_list_with(BuyerSerializer.payload)
    def get(self):
        """ Returns list of all buyers (users) """
        buyers = Buyer.query.all()
        return buyers

    @api.response(201, "Request Successful")
    @api.expect(BuyerSerializer.post_payload)
    @api.marshal_with(BuyerSerializer.payload)
    def post(self):
        """ Create new buyer (user) and posts to the
            buyer_referral entity the source does not yet exist in the DB
        """

        parsed_args = BuyerParser.post_args.parse_args(request)
        buyer = BuyerDomain.create_buyer(parsed_args)
        if buyer:
            return buyer
        api.abort(400, message='buyer already exists in the database')

@ns.route('/<int:id>')
@api.response(200, 'Request Successful')
@api.response(404, 'Not Found')
class BuyerItem(Resource):
    """ End points for ticket-vendor/buyer/id """

    @api.marshal_with(BuyerSerializer.payload)
    def get(self, id):
        """ Return buyer by id """

        buyer = Buyer.query.get_or_404(id)
        log.debug(f'SELECT buyer by id :: {id}, {repr(buyer)}')
        return buyer

