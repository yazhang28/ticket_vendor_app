# coding=utf-8
#!/usr/bin/env python3

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
    buyer_referral_type_txt = db.Column(db.VARCHAR(length=50), nullable=False)
    buyer_referral_type_id = db.Column(db.BIGINT, db.ForeignKey('buyer_referral_type.id'), nullable=False)
    buyer_referral_type = db.relationship('BuyerReferralType', backref=backref('buyer', uselist=False))
    active = db.Column(db.BOOLEAN, default=True, server_default='t', nullable=True)

    def __init__(self,
                 email_address: str,
                 first_name: str,
                 last_name: str,
                 buyer_referral_type_txt: str,
                 buyer_referral_type_id: int,
                 phone_number: str = None,
                 active: bool = None):

        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.buyer_referral_type_txt = buyer_referral_type_txt
        self.buyer_referral_type_id = buyer_referral_type_id
        self.active = active

    def __repr__(self):
        return 'Buyer (id=%r, email_address=%r,' \
               'first_name=%r, last_name=%r,' \
               'phone_number=%r, active=%r' \
               'buyer_referral_type_txt=%r, buyer_referral_type_id=%r)'\
               % (self.id, self.email_address,\
                  self.first_name, self.last_name,\
                  self.phone_number, self.buyer_referral_type_id,\
                  self.buyer_referral_type_txt, self.active)

class BuyerReferralType(db.Model):
    """ buyer_referral_type Entity """
    id = db.Column(db.BIGINT, primary_key=True)
    type = db.Column(db.VARCHAR(length=50), unique=True, nullable=False)

    def __init__(self, type: str):
        self.type = type

    def __repr__(self):
        return 'BuyerReferralType(id=%r, buyer_referral_type=%r)' % (self.id, self.type)

class BuyerPaymentMethod(db.Model):
    """ buyer_payment_method Entity """
    id = db.Column(db.BIGINT, primary_key=True)

    buyer_id = db.Column(db.BIGINT, db.ForeignKey('buyer.id'), nullable=False)
    buyer = db.relationship('Buyer', backref='buyer_payment_method')

    billing_address = db.Column(
        db.VARCHAR(100),
        db.CheckConstraint(sqltext="billing_address ~ '[\sA-Za-z0-9.]+'", name='billing_address'),
        nullable=True)
    city = db.Column(db.VARCHAR(100), nullable=True)
    postal_code = db.Column(
        db.VARCHAR(50),
        db.CheckConstraint(sqltext="postal_code ~ '[0-9]'", name='postal_code'),
        nullable=True)
    credit_card_number = db.Column(db.VARCHAR(20), nullable=True)
    security_code = db.Column(
        db.VARCHAR(4),
        db.CheckConstraint(sqltext="postal_code ~ '[0-9]'", name='security_code'),
        nullable=True)
    month_exp = db.Column(
        db.INT,
        db.CheckConstraint(sqltext="month_exp <=12 AND month_exp >= 1", name='month_exp'),
        nullable=True)
    year_exp = db.Column(
        db.BIGINT,
        db.CheckConstraint(sqltext="year_exp >= extract(YEAR FROM CURRENT_DATE)::INT", name='year_exp'),
        nullable=True)
    internal_buyer_payment_method = db.Column(
        db.BOOLEAN,
        default=False,
        server_default='f',
        nullable=True)
    external_buyer_payment_method = db.Column(
        db.Boolean,
        default=False,
        server_default='f',
        nullable=True)
    active = db.Column(db.BOOLEAN, default=True, server_default='t', nullable=True)

    def __init__(self,
                 buyer_id: int,
                 billing_address: str = None,
                 city: str = None,
                 postal_code: str = None,
                 credit_card_number: str = None,
                 security_code: str = None,
                 month_exp: int = None,
                 year_exp: int = None,
                 internal_buyer_payment_method: bool = None,
                 external_buyer_payment_method: bool = None,
                 active: bool = None):

        self.buyer_id = buyer_id
        self.billing_address = billing_address
        self.city = city
        self.postal_code = postal_code
        self.credit_card_number = credit_card_number
        self.security_code = security_code
        self.month_exp = month_exp
        self.year_exp = year_exp
        self.internal_buyer_payment_method = internal_buyer_payment_method
        self.external_buyer_payment_method = external_buyer_payment_method
        self.active = active

    def __repr__(self):
        return 'BuyerPaymentMethod(id=%r,' \
               'buyer_id=%r, billing_address=%r,' \
               'city=%r, postal_code=%r,' \
               'credit_card_number=%r, security_code=%r,' \
               'month_exp=%r, year_epx=%r,' \
               'internal_buyer_payment_method=%r, external_buyer_payment_method=%r,' \
               'active=%r)' % \
               (self.id, self.buyer_id,\
               self.billing_address, self.city,\
               self.postal_code, self.credit_card_number,\
               self.security_code, self.month_exp,\
               self.year_exp, self.internal_buyer_payment_method,\
               self.external_buyer_payment_method, self.active)

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
    delivery_by_email = db.Column(db.BOOLEAN, nullable=True)
    delivery_by_phone = db.Column(db.BOOLEAN, nullable=True)
    # db.Constraint(
    #     "(date_sold IS NULL\
    #     AND buyer_id IS NULL\
    #     AND delivery_by_email IS NULL\
    #     AND delivery_by_phone IS NULL)\
    # OR (date_sold IS NOT NULL\
    #     AND buyer_id IS NOT NULL\
    #     AND delivery_by_email IS NOT NULL\
    #     AND delivery_by_phone IS NULL)\
    # OR (date_sold IS NULL\
    #     AND buyer_id IS NOT NULL\
    #     AND delivery_by_email IS NULL\
    #     AND delivery_by_phone IS NOT NULL)", name='required_fields_for_sale')

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
