#!/usr/bin/env python3
# coding=utf-8

""" Buyer Referral Type API Endpoints """
import logging
from flask import request
from flask_restplus import Resource
from api.config import api

ns = api.namespace('ticket/buyer_referral_type', description='Operations related to ticket buyer_referral_type entity')
