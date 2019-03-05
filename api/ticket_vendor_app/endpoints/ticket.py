#!/usr/bin/env python3
# coding=utf-8

""" Buyer API Endpoints """
import logging
from flask import request
from flask_restplus import Resource, fields
from api.config import api
from api.ticket_vendor_app.business_domain import TicketDomain
from api.ticket_vendor_app.endpoints.parsers import TicketParser
from database.models import Ticket

log = logging.getLogger(__name__)
ticket_domain = TicketDomain()
ns = api.namespace('ticket-vendor/ticket',
                   description='Operations related to ticket_vendor_app ticket_vendor_app entity')

post_payload = api.model('ticket', {
    'id': fields.Integer(readOnly=True, description="Unique identifier of a ticket"),
    'event_id': fields.Integer(required=True, description='Unique identifier of an event ticket is for'),
    'buyer_id': fields.Integer(
        required=False,
        description='Unique identifier of the purchaser associated with this ticket'),
    'row': fields.String(required=True, max_length=100),
    'section': fields.Integer(required=True),
    'quantity': fields.Integer(required=True, min=1, description='Number of tickets associated with this ticket sale'),
    'price': fields.Integer(require=True, min=1),
    'sold': fields.Boolean(required=False),
    'date_sold': fields.DateTime(required=False),
    'delivery_by_mail': fields.Boolean(required=False, description='Method of ticket delivery'),
    'delivery_by_phone': fields.Boolean(required=False, description='Method of ticket delivery'),
})


put_payload = api.model('ticket', {
    'id': fields.Integer(readOnly=True, description="Unique identifier of a ticket"),
    'event_id': fields.Integer(required=False, description='Unique identifier of an event ticket is for'),
    'buyer_id': fields.Integer(
        required=False,
        description='Unique identifier of the purchaser associated with this ticket'),
    'email_address': fields.String(required=True,
                                   pattern='^[A-Za-z0-9._%-]+@[A-Za-z0-9-]+[.][A-Za-z]+$',
                                   max_length=50),
    'first_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
    'last_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
    'phone_number': fields.String(required=False, max_length=50),
    'buyer_referral_type_txt': fields.String(required=True, max_length=50),
    'row': fields.String(required=False, max_length=100),
    'section': fields.Integer(required=False),
    'quantity': fields.Integer(required=False, min=1, description='Number of tickets associated with this ticket sale'),
    'price': fields.Integer(require=False, min=1),
    'sold': fields.Boolean(required=True, default=True),
    'date_sold': fields.DateTime(required=True),
    'delivery_by_mail': fields.Boolean(required=False, description='Method of ticket delivery'),
    'delivery_by_phone': fields.Boolean(required=False, description='Method of ticket delivery'),
})

@ns.route('/')
@api.response(400, "Bad Request")
class TicketCollection(Resource):
    """ End points ticket-vendor/ticket """

    @api.marshal_list_with(post_payload)
    def get(self):
        """ Returns list of all event tickets """
        ticket = Ticket.query.all()
        return ticket

    @api.response(201, "ticket created")
    @api.expect(post_payload)
    @api.marshal_with(post_payload)
    def post(self):
        """ Create new event ticket (user) """
        parsed_args = TicketParser.post_args.parse_args(request)
        ticket = ticket_domain.create_ticket(parsed_args)
        if ticket:
            return ticket
        elif ticket is None:
            api.abort(400)

@ns.route('/<int:event_id>')
@api.response(404, 'Bad Request')
@api.response(200, 'Request Successful')
class TicketItem(Resource):
    """ End points for ticket-vendor/ticket/id """

    @api.marshal_with(post_payload)
    def get(self, event_id):
        """ Return event tickets associated to an event id """
        ticket = ticket_domain.get_ticket(event_id)
        return ticket

@ns.route('/<int:id>/')
@api.response(404, 'Bad Request')
@api.response(200, 'Request Successful')
class TicketPurchase(Resource):
    """ End points for ticket-vendor/ticket/id/buyer_id"""

    @api.marshal_with(put_payload)
    @api.expect(put_payload)
    def put(self, id):
        """ Update event ticket with purchase details """
        parse_args = TicketParser.buy_put_args.parse_args()
        log.debug(parse_args)
        ticket = ticket_domain.update_ticket(id, parse_args)
        if ticket:
            return ticket
        elif ticket is None:
            api.abort(400)

