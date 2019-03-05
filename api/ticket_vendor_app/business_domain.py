#!/usr/bin/env python3.7
# coding=utf-8

""" Domain logic """
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from database import db
from database.models import Buyer, BuyerReferral, City, Event, Ticket

log = logging.getLogger(__name__)

class BuyerDomain:
    """ Domain logic for buyer Entity """

    @staticmethod
    def create_buyer(data):
        """ Creates new buyer and post to DB """
        log.debug(f'checking if already exists in buyer :: parsed args :: {data}')

        # check if user exists
        buyer = Buyer.query.filter_by(email_address=data['email_address']).first()
        if not buyer:

            # check if buyer_referral exists
            buyer_referral_id = BuyerReferralDomain().\
                transform_buyer_referral(data['buyer_referral_txt'])

            if buyer_referral_id is None:
                buyer_referral_id = BuyerReferralDomain.create_buyer_referral(data['buyer_referral_txt']).id

            buyer = Buyer(email_address=data["email_address"],
                          first_name=data["first_name"],
                          last_name=data["last_name"],
                          buyer_referral_txt=data['buyer_referral_txt'],
                          buyer_referral_id=buyer_referral_id)
            log.debug(f'INSERT to buyer Entity :: {repr(buyer)}')
            db.session.add(buyer)
            db.session.commit()
            return buyer
        log.debug(f'buyer already exists!')
        return None

#TODO: refactor Type domains
class BuyerReferralDomain:
    """ Domain logic for buyer_referral Entity """

    @staticmethod
    def transform_buyer_referral(data: str) -> int:
        """ Transform incoming buyer_referral_id to match DB schema """
        log.debug(f'transforming buyer_referral :: {data}')

        mapping = {buyer_referral.type: buyer_referral.id for buyer_referral in BuyerReferral.query.all()}
        log.debug(f'buyer_referral mapping :: {mapping}')

        return mapping[data] if data in mapping else None

    @staticmethod
    def create_buyer_referral(data):
        """ Creates new buyer_referral and post to DB """

        log.debug(f'checking if already exists in buyer_referral :: parsed data :: {data}')
        data = data['type'].lower()
        buyer_referral = BuyerReferral.query. \
            filter_by(type=data).first()

        # log.debug(f'checking buyer_referral :: {repr(buyer_referral)}')

        if not buyer_referral:
            buyer_referral = BuyerReferral(type=data)
            log.debug(f'adding to buyer_referral :: {buyer_referral.type}')
            db.session.add(buyer_referral)
            db.session.commit()

            log.debug(f'INSERT to buyer_referral Entity :: {repr(buyer_referral)}')
            return buyer_referral
        log.debug(f'buyer_type_referral already exists!')
        return None

#TODO: refactor Type domains
class CityDomain:
    """ Domain logic for city Entity """

    @staticmethod
    def transform_city(data: str) -> int:
        """ Transform incoming city_id to match DB schema """
        log.debug(f'transforming city :: {data}')

        mapping = {city.name: city.id for city in City.query.all()}
        log.debug(f'city mapping :: {mapping}')

        return mapping[data] if data in mapping else None

    @staticmethod
    def create_city(data):
        """ Creates new city and post to DB """

        log.debug(f'checking if already exists in city :: parsed data :: {data}')
        data = data['name'].lower()

        city = City.query. \
            filter_by(name=data).first()

        log.debug(f'checking city :: {repr(city)}')

        if not city:
            city = City(name=data)
            # log.debug(f'adding to city Entity :: {buyer_referral.type}')
            log.debug(f'INSERT to city Entity :: {repr(city)}')
            db.session.add(city)
            db.session.commit()
            return city
        log.debug(f'city already exists!')
        return None

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

        # check if city exists
        log.debug(f'checking if already exists in event :: parsed data :: {data}')

        # check if event already exists
        id = data['event_id']
        event = Event.query.filter_by(event_id=id).first()
        if not event:
            city_id = CityDomain().transform_city(data['city_txt'])

            if city_id is None:
                city = {'name': data['city_txt']}
                city_id = CityDomain().create_city(city).id

            event = Event(event_id=data['event_id'],
                          date=data['date'],
                          city_txt=data['city_txt'],
                          city_id=city_id)

            log.debug(f'INSERT to event Entity :: {repr(event)}')
            db.session.add(event)
            db.session.commit()
            return event
        log.debug(f'Event already exists!')
        return None

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
        id = CityDomain.transform_city(city)

        if id:
            subquery = Event.query.filter_by(city_id=id)
            if month is None:
                log.debug(f'SELECT event :: {repr(subquery)} by city :: {city} :: id :: {id}')
                return subquery.all()

            current_date = datetime.utcnow().date()
            future_date = current_date + relativedelta(months=+6)

            result = Event.query \
                .filter(Event.city_id == id) \
                .filter(Event.date >= current_date) \
                .filter(Event.date <= future_date) \
                .all()

            if result:
                log.debug(f'SELECT event :: {repr(result)} by city :: {city} :: in dates :: {current_date} - {future_date}')
                return result
            log.debug(f'No events found for city :: {city} in specified range :: {current_date} - {future_date}')
        else:
            log.debug(f'City has not been added yet!')
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

        raise NotImplementedError

    @staticmethod
    def get_ticket(id: int):
        """ Returns ticket by event_id """

        result = Ticket.query.filter_by(event_id=id).all()
        log.debug(f'SELECT ticket by event_id :: {id}, {repr(result)}')
        return result

    @staticmethod
    def update_ticket(id: int, data):
        """ Updates existing event when purchased """

        # check if ticket exists
        log.debug(f'checking if already ticket exists :: parsed data :: {data}')
        ticket = Ticket.query.get_or_404(id)

        log.debug(f'Checking for buyer data :: {data}')
        if 'buyer_id' not in data:
            buyer_data = {'email_address': data['email_address'],
                          'first_name': data['first_name'],
                          'last_name': data['last_name'],
                          'buyer_referral_txt': data['buyer_referral']
                          }
            if 'phone_number' in data:
                buyer_data['phone_number'] = data['phone_number']
            buyer_id = BuyerDomain().create_buyer(buyer_data).id

        if 'delivery_by_phone' in data:
            ticket.delivery_by_phone = data['delivery_by_phone']
        if 'delivery_by_email' in data:
            ticket.delivery_by_email = data['delivery_by_email']

        ticket.buyer_id = buyer_id
        ticket.sold = data['sold']
        ticket.date_sold = datetime.utcnow()

        log.debug(f'UPDATING ticket record with buyer info :: {repr(ticket)}')
        db.session.commit()
        return ticket


