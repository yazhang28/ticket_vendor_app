# coding=utf-8
#!/usr/bin/env python3

""" Class of DB entity models """
from datetime import datetime
from database import db

class Buyer(db.Model):
    """ Buyer Entity """
    id = db.Column(db.BIGINT, primary_key=True)
    email_address = db.Column(db.VARCHAR(length=50), unique=True, nullable=False)
    buyer_referral_type_id = db.Column(db.BIGINT, db.ForeignKey('buyer_referral_type.id'), nullable=True)
    buyer_referral_type_id = db.relationship

class BuyerReferralType(db.Model):
    """ buyer_referral_type Entity """
    id = db.Column(db.BIGINT, primary_key=True)
    type = db.Column(db.VARCHAR(length=50), unique=True, nullable=False)

class PaymentMethod(db.Model):
    """ payment_method Entity """
    id = db.Column(db.BIGINT, primary_key=True)
    buyer_id = db.Column(db.BIGINT, db.ForeignKey('buyer.id'), nullable=False)
    billing_address = db.Column(db.VARCHAR(100), nullable=True)
    city = db.Column(db.VARCHAR(100), nullable=True)
    postal_code = db.Column(db.VARCHAR(50), nullable=True)
    credit_card_number = db.Column(db.VARCHAR(20), nullable=True)
    security_code = db.Column(db.VARCHAR(4), nullable=True)
    month_exp = db.Column(db.INT, nullable=True)
    year_exp = db.Column(db.BIGINT, nullable=True)
    internal_payment_method = db.Column(db.BOOLEAN)
    external_payment_method

class City(db.Model):
    """ city Entity"""
    id = db.Column(db.BIGINT, primary_key=True)
    city = db.Column(db.VARCHAR(100), unique=True, nullable=False)

class Event(db.Model):
    """ event Entity """
    id = db.Column(db.BIGINT, primary_key=True)
    date = db.Column(db.DATE, nullable=False)
    time = db.Column(db.TIME, nullable=False)
    city_id = db.Column(db.BIGINT, db.ForeignKey('city.id'), nullable=False)

class Ticket(db.Model):
    """ ticket Entity """
    id = db.Column(db.BIGINT, primary_key=True)

