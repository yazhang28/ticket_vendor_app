#!/usr/bin/env python3.7
# coding=utf-8
""" database package """
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def reset_database():
    """ Do a clean creation of the DB Schema """
    
    db.drop_all()
    db.create_all()
