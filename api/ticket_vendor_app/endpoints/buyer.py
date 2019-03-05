#!/usr/bin/env python3
# coding=utf-8

""" Buyer Endpoints """
import logging
from flask import request
from flask_restplus import Resource, fields
from api.config import api
from api.ticket_vendor_app.business_domain import BuyerDomain
from api.ticket_vendor_app.endpoints.parsers import BuyerParser
from database.models import Buyer
from database import db

log = logging.getLogger(__name__)
buyer_domain = BuyerDomain()
ns = api.namespace('ticket-vendor/buyer', description='Operations related to ticket_vendor_app: Buyer entity')

post_payload = api.model('buyer', {
    'id': fields.Integer(readOnly=True, description="Unique identifier of a Buyer"),
    'email_address': fields.String(required=True,
                                   pattern='^[A-Za-z0-9._%-]+@[A-Za-z0-9-]+[.][A-Za-z]+$',
                                   max_length=50),
    'first_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
    'last_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
    'phone_number': fields.String(required=False, max_length=50),
    'buyer_referral_txt': fields.String(required=True, max_length=50),
    'buyer_referral_id': fields.Integer(readOnly=True, required=False),
    'active': fields.Boolean(default=True, required=False)
})

@ns.route('/')
@api.response(400, "Bad Request")
class BuyerCollection(Resource):
    """ End points ticket-vendor/buyer """

    @api.marshal_list_with(post_payload)
    def get(self):
        """ Returns list of all buyers (users) """
        buyers = Buyer.query.all()
        return buyers

    @api.response(201, "buyer created")
    @api.expect(post_payload)
    @api.marshal_with(post_payload)
    def post(self):
        """ Create new buyer (user) """
        parsed_args = BuyerParser.post_args.parse_args(request)

        log.debug(f'checking if already exists in buyer :: parsed args :: {parsed_args}')
        buyer = BuyerDomain.check_buyer(parsed_args['email_address'])
        if not buyer:
            buyer = buyer_domain.create_buyer(parsed_args)
            return buyer
        log.debug(f'buyer already exists!')
        api.abort(400)

@ns.route('/<int:id>')
@api.response(200, 'Request Successful')
@api.response(404, 'Bad Request')
class BuyerItem(Resource):
    """ End points for ticket-vendor/buyer/id """

    @api.marshal_with(post_payload)
    def get(self, id):
        """ Return buyer by id """

        buyer = Buyer.query.get_or_404(id)
        log.debug(f'SELECT buyer by id :: {id}, {repr(buyer)}')
        return buyer

