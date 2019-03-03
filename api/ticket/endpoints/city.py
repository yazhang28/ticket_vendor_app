#!/usr/bin/env python3
# coding=utf-8

""" City API Endpoints """
import logging
from flask import request
from flask_restplus import Resource
from api.config import api

ns = api.namespace('ticket/city', description='Operations related to city entity')
