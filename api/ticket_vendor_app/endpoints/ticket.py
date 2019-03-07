#!/usr/bin/env python3.7
# coding=utf-8

""" Buyer API Endpoints """
import logging
from flask import request
from flask_restplus import Resource
from api.config import api
from api.ticket_vendor_app.business_domain import TicketDomain
from api.ticket_vendor_app.endpoints.parsers import TicketParser
from api.ticket_vendor_app.endpoints.serializers import TicketSerializer
from database.models import Ticket

log = logging.getLogger(__name__)
ns = api.namespace('ticket-vendor/ticket',
                   description='Operations related to the ticket ticket_vendor_app entity')

@ns.route('/')
@api.response(400, "Bad Request")
class TicketCollection(Resource):
    """ End points ticket-vendor/ticket """

    @api.marshal_list_with(TicketSerializer.get_payload)
    def get(self):
        """ Returns list of all event tickets """

        ticket = Ticket.query.all()
        return ticket

    @api.response(201, "ticket created")
    @api.expect(TicketSerializer.post_payload)
    @api.marshal_with(TicketSerializer.get_payload)
    def post(self):
        """ Create new event ticket """

        parsed_args = TicketParser.post_args.parse_args(request)
        ticket = TicketDomain.create_ticket(parsed_args)
        if ticket:
            return ticket
        elif ticket is None:
            api.abort(400)

@ns.route('/<int:event_id>/<int:quantity>')
@api.response(404, 'Not Found')
@api.response(200, 'Request Successful')
class TicketItem(Resource):
    """ End points for ticket-vendor/ticket/id """

    @api.marshal_with(TicketSerializer.get_payload)
    def get(self, event_id, quantity):
        """ Return "best value" tickets for an event that also satisfies specified quantity """
        ticket = TicketDomain.get_ticket(event_id, quantity)
        return ticket

@ns.route('/<int:id>/')
@api.response(404, 'Not Found')
@api.response(200, 'Request Successful')
class TicketPurchase(Resource):
    """ End points for ticket-vendor/ticket/id/buyer_id"""

    @api.marshal_with(TicketSerializer.get_payload)
    @api.expect(TicketSerializer.put_payload)
    def put(self, id):
        """ Update event ticket with purchase details """

        parse_args = TicketParser.buy_put_args.parse_args()
        ticket = TicketDomain.update_ticket(id, parse_args)
        if ticket:
            return ticket
        elif ticket is None:
            api.abort(404, "Unable to update ticket record, ticket not exist or has already been set to SOLD status")

