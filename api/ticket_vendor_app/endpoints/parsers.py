#!/usr/bin/env python3.7
# coding=utf-8
from datetime import datetime
from flask_restful import reqparse

class BuyerParser:
    """ Class of parameter parsers for the Buyer Entity """
    # get_args = reqparse.RequestParser()
    # get_args.add_argument('id', required=True, type=int)

    post_args = reqparse.RequestParser()
    post_args.add_argument('email_address', required=True, type=str)
    post_args.add_argument('first_name', required=True, type=str)
    post_args.add_argument('last_name', required=True, type=str)
    post_args.add_argument('phone_number', required=False, type=str)
    post_args.add_argument('buyer_referral_txt', required=True, type=str)

#TODO: refactor type parser
class BuyerReferralParser:
    """ Class of parameter parsers for the buyer_referral Entity """
    args = reqparse.RequestParser()
    args.add_argument('type', required=True, type=str)

class CityParser:
    """ Class of parameter parsers for the city Entity """
    args = reqparse.RequestParser()
    args.add_argument('name', required=True, type=str)

class EventParser:
    """ Class of parameter parsers for the event Entity """
    post_args = reqparse.RequestParser()
    post_args.add_argument('event_id', required=True, type=int)
    post_args.add_argument('city_txt', required=True, type=str)
    post_args.add_argument('date', required=True, type=lambda x: datetime.strptime(x, '%d-%m-%Y'))

    get_args = post_args.copy()
    get_args.remove_argument('date')

    # get_args = reqparse.RequestParser()
    # get_args.add_argument('city_txt', required=True, type=str)
    # get_args.add_argument('event_id', required=True, type=int)

class TicketParser:
    """ Class of parameter parsers for the ticket Entity """
    post_args = reqparse.RequestParser()
    # post_args.add_argument('event_id', required=True, type=int)
    post_args.add_argument('row', required=True, type=str)
    post_args.add_argument('section', required=True, type=int)
    post_args.add_argument('quantity', required=True, type=int)
    post_args.add_argument('price', required=True, type=int)

    buy_put_args = BuyerParser.post_args.copy()
    buy_put_args.add_argument('sold', required=True, type=bool)


