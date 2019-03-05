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
ns = api.namespace('ticket_vendor_app/buyer', description='Operations related to ticket_vendor_app: buyer entity')

post_payload = api.model('buyer', {
    'id': fields.Integer(readOnly=True, description="Unique identifier of a buyer"),
    'email_address': fields.String(required=True,
                                   pattern='^[A-Za-z0-9._%-]+@[A-Za-z0-9-]+[.][A-Za-z]+$',
                                   max_length=50),
    'first_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
    'last_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
    'phone_number': fields.String(required=False, max_length=50),
    'buyer_referral_type_txt': fields.String(required=True, max_length=50),
    'buyer_referral_type_id': fields.Integer(required=False),
    'active': fields.Boolean(default=True, required=False)
})

@ns.route('/')
@api.response(400, "Bad Request")
class BuyerCollection(Resource):
    """ End points ticket_vendor_app/buyer """

    @api.marshal_list_with(post_payload)
    # @api.expect(BuyerSerializer.post_payload)
    def get(self):
        """ Returns list of buyers (users) """
        buyers = Buyer.query.all()
        return buyers

    @api.response(201, "buyer created")
    @api.expect(post_payload)
    @api.marshal_with(post_payload)
    def post(self):
        """ Create new buyer (user) """
        parsed_args = BuyerParser.post_args.parse_args(request)
        buyer = buyer_domain.create_buyer(parsed_args)
        if buyer:
            return buyer, 201
        elif buyer is None:
            api.abort(400)

@ns.route('/<int:id>')
@api.response(404, 'Bad Request')
class BuyerItem(Resource):
    """ End points for ticket_vendor_app/buyer/id """

    @api.marshal_with(post_payload)
    def get(self, id):
        """ Return buyer by Id """

        result = Buyer.query.get_or_404(id)
        log.debug(f'SELECT buyer by id :: {id}, {repr(result)}')
        return result

    @api.marshal_with(post_payload)
    @api.response(200, "Request Successful")
    def put(self, id):
        """ Update existing buyer - out of scope """
        raise NotImplementedError



