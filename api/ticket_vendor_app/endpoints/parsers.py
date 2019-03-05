#!/usr/bin/env python3.7
# coding=utf-8
import datetime
from flask_restful import reqparse

class BuyerParser:
    """ Class of parameter parsers for the Buyer Entity """
    get_args = reqparse.RequestParser()
    get_args.add_argument('id', required=True, type=int)

    post_args = reqparse.RequestParser()
    post_args.add_argument('email_address', required=True, type=str)
    post_args.add_argument('first_name', required=True, type=str)
    post_args.add_argument('last_name', required=True, type=str)
    post_args.add_argument('phone_number', required=False, type=str)
    post_args.add_argument('buyer_referral_type_txt', required=True, type=str)

#TODO: refactor type parser
class BuyerReferralTypeParser:
    """ Class of parameter parsers for the buyer_referral_type Entity """
    args = reqparse.RequestParser()
    args.add_argument('type', required=True, type=str)

class CityParser:
    """ Class of parameter parsers for the buyer_referral_type Entity """
    args = reqparse.RequestParser()
    args.add_argument('name', required=True, type=str)

class EventParser:
    """ Class of parament parsers for the event Entity """
    post_args = reqparse.RequestParser()
    post_args.add_argument('event_id', required=True, type=int)
    post_args.add_argument('date', required=True, type=lambda x: reqparse.date(x))

