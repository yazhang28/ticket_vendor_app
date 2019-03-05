# coding=utf-8
""" TODO: add docstring """
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def reset_database():
    """ Do a clean creation of the DB Schema """
    from .models import Buyer, BuyerReferral, BuyerPaymentMethod, City, Event, Ticket
    db.drop_all()
    db.create_all()
