#!/usr/bin/env python3
# coding=utf-8

""" Buyer Referral Type API Endpoints """
import logging
from flask import request
from flask_restplus import Resource, fields
from api.config import api
from api.ticket_vendor_app.endpoints.parsers import BuyerReferralTypeParser
from api.ticket_vendor_app.business_domain import BuyerReferralTypeDomain
from database.models import BuyerReferralType

log = logging.getLogger(__name__)
ns = api.namespace('ticket_vendor_app/buyer_referral_type', description='Operations related to ticket_vendor_app: buyer_referral_type entity')
buyer_referral_type_domain = BuyerReferralTypeDomain()

post_payload = api.model('buyer_referral_type', {
    'id': fields.Integer(readOnly=True, description="Unique identifier of a buyer_referral_type"),
    'type': fields.String(required=True, description='vendor referral source used by buyer')
})

@ns.route('/')
@api.response(404, "Bad Request")
class BuyerReferralTypeCollection(Resource):
    """ End points ticket_vendor_app/buyer_referral_type """

    @api.marshal_list_with(post_payload)
    def get(self):
        """ Returns list of referral types """

        buyer_referral_type = BuyerReferralType.query.all()
        return buyer_referral_type

    @api.response(201, "buyer_referral_type created")
    @api.expect(post_payload)
    @api.marshal_with(post_payload)
    def post(self):
        """ Creates new buyer_referral_type """

        parsed_args = BuyerReferralTypeParser.args.parse_args(request)
        buyer_referral_type = buyer_referral_type_domain.create_buyer_referral_type(parsed_args)
        if buyer_referral_type:
            return buyer_referral_type, 201
        api.abort(404)

@ns.route('/<int:id>')
@api.response(200, 'Request Successful')
@api.response(404, 'Bad Request')
class BuyerReferralTypeItem(Resource):
    """ End points for ticket_vendor_app/buyer_referral_type/id """

    @api.marshal_with(post_payload)
    def get(self, id):
        """ Return buyer_referral_type by Id """

        result = BuyerReferralType.query.get_or_404(id)
        log.debug(f'SELECT buyer_referral_type by id :: {id}, {repr(result)}')
        return result
