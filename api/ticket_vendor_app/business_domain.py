#!/usr/bin/env python3.7.7
# coding=utf-8

""" Domain logic """
from typing import Dict
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from sqlalchemy import func

from database import db
from database.models import Buyer, BuyerReferral, City, Event, Ticket

log = logging.getLogger(__name__)

class BuyerDomain:
    """ Domain logic for buyer Entity """

    @staticmethod
    def create_buyer(data: Dict):
        """ Creates new buyer and post to DB """

        buyer = BuyerDomain.check_buyer(data['email_address'])

        if buyer:
            log.debug(f'buyer record already exists in the database :: {repr(buyer)}')
            return None

        buyer_referral_txt = data['buyer_referral_txt'].lower().replace(" ", "")
        buyer_referral = BuyerReferralDomain.\
            check_buyer_referral(buyer_referral_txt)

        if buyer_referral is None:
            buyer_referral_id = BuyerReferralDomain.create_buyer_referral(
                {'type': buyer_referral_txt}).id
        else:
            buyer_referral_id = buyer_referral.id

        buyer = Buyer(email_address=data["email_address"],
                      first_name=data["first_name"],
                      last_name=data["last_name"],
                      buyer_referral_txt=data['buyer_referral_txt'],
                      buyer_referral_id=buyer_referral_id)

        log.debug(f'INSERT to buyer Entity :: {repr(buyer)}')
        db.session.add(buyer)
        db.session.commit()
        return buyer

    @staticmethod
    def check_buyer(data: str):
        """ Check for existing buyer record in DB by email_address """

        log.debug(f'checking for existing buyer record :: parsed args :: {data}')
        buyer = Buyer.query.filter_by(email_address=data).first()

        log.debug(f'buyer record found :: {repr(buyer)}')
        return buyer

#TODO: refactor Type domains
class BuyerReferralDomain:
    """ Domain logic for buyer_referral Entity """

    @staticmethod
    def check_buyer_referral(data: str):
        """ Checks for buyer_referral record in DB by referral_type_txt """

        buyer_referral = BuyerReferral.query. \
            filter_by(type=data).first()

        if buyer_referral:
            log.debug(f'buyer_referral record found :: {repr(buyer_referral)}')
            return buyer_referral
        return None

    @staticmethod
    def create_buyer_referral(data: Dict):
        """ Creates new buyer_referral and post to DB
            :param : data (format)
                {'type': <buyer_referrral_txt>}
        """

        log.debug(f'checking if already exists in buyer_referral :: parsed data :: {data}')

        data = data['type']
        buyer_referral = BuyerReferralDomain.check_buyer_referral(data)

        if buyer_referral:
            log.debug(f'buyer_type_referral record already exists :: {repr(buyer_referral)}')
            return None

        buyer_referral = BuyerReferral(type=data)
        log.debug(f'adding to buyer_referral :: {buyer_referral.type}')
        db.session.add(buyer_referral)
        db.session.commit()

        log.debug(f'INSERT to buyer_referral Entity :: {repr(buyer_referral)}')
        return buyer_referral

#TODO: refactor Type domains
class CityDomain:
    """ Domain logic for city Entity """

    @staticmethod
    def check_city(data: str) -> int:
        """ Checks for city record in DB by name """
        data.lower().replace(" ", "")
        city = City.query.filter_by(name=data).first()

        if city:
            log.debug(f'city record found :: {repr(city)}')
            return city.id
        return None

    @staticmethod
    def create_city(data: Dict):
        """ Creates new city and post to DB
            :param : data (format)
                {'name': <name>}
        """

        log.debug(f'Checking city record already exists in db :: parsed data :: {data}')

        city_name = data['name'].lower().replace(" ", "")
        city_id = CityDomain.check_city(city_name)

        if city_id:
            return None

        city = City(name=city_name)
        log.debug(f'INSERT to city Entity :: {repr(city)}')
        db.session.add(city)
        db.session.commit()
        return city

    @staticmethod
    def get_city(id: int):
        """ Returns city by id """

        result = City.query.get_or_404(id)
        log.debug(f'SELECT City by id :: {id}, {repr(result)}')
        return result

class EventDomain:
    """ Domain logic for buyer Entity """

    @staticmethod
    def create_event(data):
        """ Creates new buyer and post to DB """

        log.debug(f'Checking event record already exists in db :: parsed data :: {data}')
        id = data['event_id']
        event = Event.query.filter_by(event_id=id).first()

        if event:
            log.debug(f'Event record already exists in the database :: {repr(event)}')
            return None

        city_txt = data['city_txt'].lower().replace(" ", "")
        city_id = CityDomain.check_city(city_txt)

        if city_id is None:
            city = {'name': city_txt}
            city_id = CityDomain.create_city(city).id

        event = Event(event_id=data['event_id'],
                      date=data['date'],
                      city_txt=data['city_txt'],
                      city_id=city_id)

        log.debug(f'INSERT to event Entity :: {repr(event)}')
        db.session.add(event)
        db.session.commit()
        return event

    @staticmethod
    def get_event(id: int):
        """ Returns event by id """

        result = Event.query.get_or_404(id)
        log.debug(f'SELECT Event by id :: {id}, {repr(result)}')
        return result

    @staticmethod
    def get_event_batch(city: str, month: int = None):
        """ Returns event by city, narrow down by date (optional) """

        # retrieve city id from city entity
        id = CityDomain.check_city(city)

        if id:
            subquery = Event.query.filter_by(city_id=id)
            log.debug
            if month is None:
                log.debug(f'SELECT event :: {repr(subquery)} by city :: {city} :: id :: {id}')
                return subquery.all()

            current_date = datetime.utcnow().date()
            future_date = current_date + relativedelta(months=month)

            result = Event.query \
                .filter(Event.city_id == id) \
                .filter(Event.date >= current_date) \
                .filter(Event.date <= future_date) \
                .all()

            if result:
                log.debug(f'SELECT event :: {repr(result)} by city :: {city} :: in range :: {current_date} - {future_date}')
                return result
            log.debug(f'No events found for city :: {city} in specified range :: {current_date} - {future_date}')
        else:
            log.debug(f'No event for this city has been added yet')
        return []

class TicketDomain:
    """ Domain logic for ticket Entity """

    @staticmethod
    def create_ticket(data):
        """ Creates new ticket and post to DB """

        ticket = Ticket(event_id=data['event_id'],
                        row=data['row'],
                        section=data['section'],
                        quantity=data['quantity'],
                        price=data['price'])

        log.debug(f'INSERT to event Entity :: {repr(ticket)}')
        db.session.add(ticket)
        db.session.commit()
        return ticket

    @staticmethod
    def get_ticket(id: int, quantity: int):
        """ Returns ticket by event_id """

        subquery = db.session.query(func.min(Ticket.price)).filter(Ticket.event_id == id,
                                                                 Ticket.quantity == quantity, Ticket.sold != False).subquery()
        log.debug(f'subquery :: {repr(subquery)}')
        result = db.session.query(Ticket).filter(Ticket.event_id == id, Ticket.quantity == quantity, Ticket.sold != False,
                                                 Ticket.price.in_(subquery)).first()

        log.debug(f'SELECT ticket by event_id :: {id}, {repr(result)}')
        return result

    @staticmethod
    def update_ticket(id: int, data):
        """ Updates existing event when purchased """

        log.debug(f'Checking if ticket exists and open for sale :: parsed data :: {data}')
        ticket = Ticket.query.filter(Ticket.id == id, Ticket.sold == False).first()

        if not ticket:
            log.debug(f'Ticket does not exist or has been sold')
            return None

        buyer = BuyerDomain.check_buyer(data['email_address'])
        if buyer:
            ticket.buyer_id = buyer.id
            buyer.first_name = data['first_name']
            buyer.last_name = data['last_name']

        else:
            # Create new buyer record
            buyer_data = {'email_address': data['email_address'],
                          'first_name': data['first_name'],
                          'last_name': data['last_name'],
                          'buyer_referral_txt': data['buyer_referral_txt']
                          }
            if 'phone_number' in data:
                buyer_data['phone_number'] = data['phone_number']

            buyer_id = BuyerDomain.create_buyer(buyer_data).id
            ticket.buyer_id = buyer_id

        ticket.delivery_by_phone = data['delivery_by_phone']
        ticket.delivery_by_email = data['delivery_by_email']
        ticket.sold = data['sold']
        ticket.date_sold = datetime.utcnow()

        log.debug(f'UPDATING ticket record with buyer info :: {repr(ticket)}')
        db.session.commit()
        return ticket


