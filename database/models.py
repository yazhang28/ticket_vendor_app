#!/usr/bin/env python3.7
# coding=utf-8

""" Class of DB entity models """
from datetime import datetime
from database import db
from sqlalchemy.orm import backref

class Buyer(db.Model):
    """ Buyer Entity """
    id = db.Column(db.BIGINT, primary_key=True)
    email_address = db.Column(
        db.VARCHAR(length=50),
        db.CheckConstraint(
            sqltext="email_address ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9-]+[.][A-Za-z]+$'",
            name='email_address'),
        unique=True,
        nullable=False)
    first_name = db.Column(
        db.VARCHAR(length=50),
        db.CheckConstraint(sqltext="first_name ~* '[a-zA-Z]+'", name='first_name'),
        nullable=False)
    last_name = db.Column(
        db.VARCHAR(length=50),
        db.CheckConstraint(sqltext="first_name ~* '[a-zA-Z]+'", name='last_name'),
        nullable=False)
    phone_number = db.Column(db.VARCHAR(length=50), nullable=True)
    buyer_referral_txt = db.Column(db.VARCHAR(length=50), nullable=False)
    buyer_referral_id = db.Column(db.BIGINT, db.ForeignKey('buyer_referral.id'), nullable=False)
    buyer_referral = db.relationship('BuyerReferral', backref=backref('buyer', uselist=False))
    active = db.Column(db.BOOLEAN, default=True, server_default='t', nullable=True)

    def __init__(self,
                 email_address: str,
                 first_name: str,
                 last_name: str,
                 buyer_referral_txt: str,
                 buyer_referral_id: int,
                 phone_number: str = None,
                 active: bool = None):

        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.buyer_referral_txt = buyer_referral_txt
        self.buyer_referral_id = buyer_referral_id
        self.active = active

    def __repr__(self):
        return 'Buyer (id=%r, email_address=%r,' \
               'first_name=%r, last_name=%r,' \
               'phone_number=%r, active=%r' \
               'buyer_referral_txt=%r, buyer_referral_id=%r)'\
               % (self.id, self.email_address,\
                  self.first_name, self.last_name,\
                  self.phone_number, self.buyer_referral_id,\
                  self.buyer_referral_txt, self.active)

class BuyerReferral(db.Model):
    """ buyer_referral Entity """
    id = db.Column(db.BIGINT, primary_key=True)
    type = db.Column(db.VARCHAR(length=50), unique=True, nullable=False)

    def __init__(self, type: str):
        self.type = type

    def __repr__(self):
        return 'BuyerReferral(id=%r, buyer_referral=%r)' % (self.id, self.type)

class City(db.Model):
    """ city Entity"""
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.VARCHAR(100), unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return 'City(id=%r, name=%r)' % (self.id, self.name)

class Event(db.Model):
    """ event Entity """
    event_id = db.Column(db.BIGINT, primary_key=True, autoincrement=False)
    date = db.Column(db.DATE, nullable=False)
    city_txt = db.Column(db.VARCHAR(100), nullable=False)
    city_id = db.Column(db.BIGINT, db.ForeignKey('city.id'), nullable=False)
    city = db.relationship('City', backref=backref('event', uselist=False))

    def __init__(self, event_id: int, date: datetime, city_txt: str, city_id: int):
        self.event_id = event_id
        self.date = date,
        self.city_txt = city_txt
        self.city_id = city_id

    def __repr__(self):
        return 'Event(event_id=%r, date=%r, city_txt=%r, city_id=%r)'\
               % (self.event_id, self.date, self.city_txt, self.city_id)

class Ticket(db.Model):
    """ ticket Entity """
    id = db.Column(db.BIGINT, primary_key=True)

    event_id = db.Column(db.BIGINT, db.ForeignKey('event.event_id'), nullable=False)
    event = db.relationship('Event', backref='ticket')

    buyer_id = db.Column(db.BIGINT, db.ForeignKey('buyer.id'), nullable=True)
    buyer = db.relationship('Buyer', backref='ticket')

    row = db.Column(db.VARCHAR(5), nullable=False)
    section = db.Column(db.INT, nullable=False)
    quantity = db.Column(db.INT, nullable=False)
    price = db.Column(db.INT, nullable=False)
    sold = db.Column(db.BOOLEAN, default=False, server_default='f', nullable=False)
    date_sold = db.Column(db.TIMESTAMP, nullable=True)
    delivery_by_email = db.Column(db.BOOLEAN, default=False, nullable=False)
    delivery_by_phone = db.Column(db.BOOLEAN, default=False, nullable=False)

    def __init__(self,
                 event_id: int,
                 row: str,
                 section: int,
                 quantity: int,
                 price: int,
                 sold: bool = None,
                 buyer_id: int = None,
                 date_sold: datetime = None,
                 delivery_by_email: bool = None,
                 delivery_by_phone: bool = None):
        self.event_id = event_id
        self.buyer_id = buyer_id
        self.row = row
        self.section = section
        self.quantity = quantity
        self.price = price
        self.sold = sold
        self.date_sold = date_sold
        self.delivery_by_email = delivery_by_email
        self.delivery_by_phone = delivery_by_phone

    def __repr__(self):
        return 'Ticket(id=%r, event_id=%r,'\
               'buyer_id=%r, row=%r,'\
               'section=%r, quantity=%r,'\
               'price=%r, sold=%r,'\
               'date_sold=%r, delivery_by_mail=%r'\
               'delivery_by_phone=%r)'\
               % (self.id, self.event_id,\
               self.buyer_id, self.row,\
               self.section, self.quantity,\
               self.price, self.sold,\
               self.date_sold, self.delivery_by_email,\
               self.delivery_by_phone)
