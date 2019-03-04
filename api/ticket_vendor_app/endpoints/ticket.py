#!/usr/bin/env python3
# coding=utf-8

""" Buyer API Endpoints """
import logging
from flask import request
from flask_restplus import Resource
from api.config import api

ns = api.namespace('ticket_vendor_app/ticket_vendor_app', description='Operations related to ticket_vendor_app ticket_vendor_app entity')
