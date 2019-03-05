#!/usr/bin/env python3
# coding=utf-8

""" BuyerReferral API Endpoints """
import logging
from flask import request
from flask_restplus import Resource, fields
from api.config import api
from api.ticket_vendor_app.endpoints.parsers import BuyerReferralParser
from api.ticket_vendor_app.business_domain import BuyerReferralDomain
from database.models import BuyerReferral

log = logging.getLogger(__name__)
ns = api.namespace('ticket-vendor/buyer-referral', description='Operations related to ticket_vendor_app: BuyerReferral entity')
buyer_source_domain = BuyerReferralDomain()

post_payload = api.model('buyer_referral', {
    'id': fields.Integer(readOnly=True, description="Unique identifier of a BuyerReferral"),
    'type': fields.String(required=True, max_length=50, description='vendor referral source used by buyer')
})

@ns.route('/')
@api.response(404, "Bad Request")
class BuyerReferralCollection(Resource):
    """ End points ticket-vendor/buyer-referral """

    @api.marshal_list_with(post_payload)
    def get(self):
        """ Returns list of all buyer referrals """

        buyer_source = BuyerReferral.query.all()
        return buyer_source

    @api.response(201, "BuyerReferral created")
    @api.expect(post_payload)
    @api.marshal_with(post_payload)
    def post(self):
        """ Creates new buyer referral """

        parsed_args = BuyerReferralParser.args.parse_args(request)
        buyer_source = buyer_source_domain.create_buyer_source(parsed_args)
        if buyer_source:
            return buyer_source
        api.abort(404)

@ns.route('/<int:id>')
@api.response(200, 'Request Successful')
@api.response(404, 'Bad Request')
class BuyerReferralItem(Resource):
    """ End points for ticket-vendor/buyer-referral/id """

    @api.marshal_with(post_payload)
    def get(self, id):
        """ Return BuyerReferral by Id """

        buyer_referral = BuyerReferral.query.get_or_404(id)
        log.debug(f'SELECT BuyerReferral by id :: {id}, {repr(buyer_referral)}')
        return buyer_referral
