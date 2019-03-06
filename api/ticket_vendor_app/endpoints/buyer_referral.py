#!/usr/bin/env python3.7
# coding=utf-8

""" BuyerReferral API Endpoints """
import logging
from flask import request
from flask_restplus import Resource
from api.config import api
from api.ticket_vendor_app.endpoints.parsers import BuyerReferralParser
from api.ticket_vendor_app.endpoints.serializers import BuyerReferralSerializer
from api.ticket_vendor_app.business_domain import BuyerReferralDomain
from database.models import BuyerReferral

log = logging.getLogger(__name__)
ns = api.namespace('ticket-vendor/buyer-referral', description='Operations related to ticket_vendor_app: BuyerReferral entity')

@ns.route('/')
@api.response(400, "Bad Request")
class BuyerReferralCollection(Resource):
    """ End points ticket-vendor/buyer-referral """

    @api.marshal_list_with(BuyerReferralSerializer.payload)
    def get(self):
        """ Returns list of all buyer_referral records """

        buyer_source = BuyerReferral.query.all()
        return buyer_source

    @api.response(201, "Request Successful")
    @api.expect(BuyerReferralSerializer.payload)
    @api.marshal_with(BuyerReferralSerializer.payload)
    def post(self):
        """ Creates new buyer_referral """

        parsed_args = BuyerReferralParser.args.parse_args(request)
        buyer_source = BuyerReferralDomain.create_buyer_referral(parsed_args)
        if buyer_source:
            return buyer_source
        api.abort(400, message='buyer_referral record already exists in the database')

@ns.route('/<int:id>')
@api.response(200, 'Request Successful')
@api.response(404, 'Not Found')
class BuyerReferralItem(Resource):
    """ End points for ticket-vendor/buyer-referral/id """

    @api.marshal_with(BuyerReferralSerializer.payload)
    def get(self, id):
        """ Returns buyer_referral by id """

        buyer_referral = BuyerReferral.query.get_or_404(id)
        log.debug(f'SELECT buyer_referral by id :: {id}, {repr(buyer_referral)}')
        return buyer_referral
