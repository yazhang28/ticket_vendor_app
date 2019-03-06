#!/usr/bin/env python3.7.7
# coding=utf-8
""" Grouped Serializers """

from flask_restplus import fields
from api.config import api

class BuyerSerializer:
    """ JSON serializer variable(s) for Buyer Entity """

    post_payload = api.model('Buyer POST', {
        'id': fields.Integer(readOnly=True, description="Unique identifier of a Buyer"),
        'email_address': fields.String(required=True,
                                       pattern='^[A-Za-z0-9._%-]+@[A-Za-z0-9-]+[.][A-Za-z]+$',
                                       max_length=50),
        'first_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
        'last_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
        'phone_number': fields.String(required=False, max_length=50),
        'buyer_referral_txt': fields.String(required=True, max_length=50)
    })

    payload = api.inherit('Buyer', post_payload, {
        'buyer_referral_id': fields.Integer(readOnly=True, required=False),
        'active': fields.Boolean(default=True, required=False)
    })

class BuyerReferralSerializer:
    """ JSON serializer variable(s) for BuyerReferral Entity """

    payload = api.model('BuyerReferral POST', {
        'id': fields.Integer(readOnly=True, description="Unique identifier of a BuyerReferral"),
        'type': fields.String(required=True, max_length=50, description='Vendor referral source used by buyer')
    })

class EventSerializer:
    """ JSON serializer variable(s) for Event Entity"""

    post_payload = api.model('Event POST', {
        'event_id': fields.Integer(required=True, description='Unique identifier of an Event'),
        'date': fields.Date(required=True, description='Date of Event'),
        'city_txt': fields.String(required=True, max_length=50, description='Name of city Event takes place in')
    })

    payload = api.inherit('Event', post_payload, {
        'city_id': fields.Integer(readOnly=True, required=False, description='Id of city Event takes place in')
    })

class CitySerializer:
    """ JSON serializer variable(s) for City Entity"""

    payload = api.model('City', {
        'id': fields.Integer(readOnly=True, description="Unique identifier of a City"),
        'name': fields.String(required=True, max_length=50, description='vendor referral source used by City')
    })

class TicketSerializer:
    """ Ticker json serializer variable(s) for Ticket Entity """
    get_payload = api.model('Ticket GET', {
        'id': fields.Integer(readOnly=True, description="Unique identifier of a ticket"),
        'event_id': fields.Integer(readOnly=True, description='Unique identifier of an event ticket is for'),
        'buyer_id': fields.Integer(
            readOnly=True,
            description='Unique identifier of the purchaser associated with this ticket'),
        'row': fields.String(readOnly=True, max_length=100),
        'section': fields.Integer(readOnly=True,),
        'quantity': fields.Integer(readOnly=True, min=1, description='Number of tickets associated with this ticket sale'),
        'price': fields.Integer(readOnly=True, min=1),
        'sold': fields.Boolean(readOnly=True),
        'date_sold': fields.DateTime(readOnly=True),
        'delivery_by_mail': fields.Boolean(readOnly=True, description='Method of ticket delivery'),
        'delivery_by_phone': fields.Boolean(readOnly=True, description='Method of ticket delivery'),
    })

    post_payload = api.model('Ticket POST', {
        'id': fields.Integer(readOnly=True, description="Unique identifier of a ticket"),
        'event_id': fields.Integer(required=True, description='Unique identifier of an event ticket is for'),
        'row': fields.String(required=True, max_length=100),
        'section': fields.Integer(required=True),
        'quantity': fields.Integer(required=True, min=1, description='Number of tickets associated with this ticket sale'),
        'price': fields.Integer(required=True, min=1),
    })

    put_payload = api.model('Ticket PUT', {
        'sold': fields.Boolean(required=True, default=False),
        'delivery_by_email': fields.Boolean(default=False, description='Method of ticket delivery'),
        'delivery_by_phone': fields.Boolean(default=False, description='Method of ticket delivery'),
        'email_address': fields.String(required=True,
                                       pattern='^[A-Za-z0-9._%-]+@[A-Za-z0-9-]+[.][A-Za-z]+$',
                                       max_length=50),
        'first_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
        'last_name': fields.String(required=True, pattern='[a-zA-Z]+', max_length=100),
        'buyer_referral_txt': fields.String(required=True, max_length=50)
    })
