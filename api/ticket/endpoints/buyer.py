#!/usr/bin/env python3
# coding=utf-8

""" Buyer API Endpoints """
import logging
from flask import request
from flask_restplus import Resource
from api.config import api

ns = api.namespace('ticket/buyer', description='Operations related to ticket buyer entity')


# @ns.route('/')
# class BuyerCollection(Resource):
    # raise NotImplementedError