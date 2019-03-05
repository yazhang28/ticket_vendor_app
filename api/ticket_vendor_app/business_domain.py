#!/usr/bin/env python3.7
# coding=utf-8

""" Domain logic """
from datetime import datetime
import logging
from database import db
from database.models import Buyer, BuyerReferralType, City, Event, Ticket, BuyerPaymentMethod

log = logging.getLogger(__name__)

class BuyerDomain:
    """ Domain logic for buyer Entity """

    def create_buyer(self, data):
        """ Create new buyer and post to DB """
        log.debug(f'checking if already exists in buyer :: parsed args :: {data}')

        # check if user exists
        buyer = Buyer.query.filter_by(email_address=data['email_address']).first()
        if not buyer:

            # check if buyer_referral_type exists
            buyer_referral_type_id = BuyerReferralTypeDomain().\
                transform_buyer_referral_type(data['buyer_referral_type_txt'])

            if buyer_referral_type_id is None:
                BuyerReferralTypeDomain.create_buyer_referral_type(data['buyer_referral_type_txt'])

            buyer = Buyer(email_address=data["email_address"],
                          first_name=data["first_name"],
                          last_name=data["last_name"],
                          buyer_referral_type_txt=data['buyer_referral_type_txt'],
                          buyer_referral_type_id=buyer_referral_type_id)
            log.debug(f'INSERT to buyer Entity :: {repr(buyer)}')
            db.session.add(buyer)
            db.session.commit()
            return buyer
        log.debug(f'buyer already exists!')
        return None

#TODO: refactor Type domains
class BuyerReferralTypeDomain:
    """ Domain logic for buyer_referral_type Entity """

    def transform_buyer_referral_type(self, data: str) -> int:
        """ Transform incoming buyer_referral_type_id to match DB schema """
        log.debug(f'transforming buyer_referral_type :: {data}')

        mapping = {buyer_referral_type.type: buyer_referral_type.id for buyer_referral_type in BuyerReferralType.query.all()}
        log.debug(f'buyer_referral_type mapping :: {mapping}')

        return mapping[data] if data in mapping else None

    def create_buyer_referral_type(self, data):
        """ Create new buyer_referral_type and post to DB """

        log.debug(f'checking if already exists in buyer_referral_type :: parsed data :: {data}')
        data = data['type'].lower()
        buyer_referral_type = BuyerReferralType.query. \
            filter_by(type=data).first()

        # log.debug(f'checking buyer_referral_type :: {repr(buyer_referral_type)}')

        if not buyer_referral_type:
            buyer_referral_type = BuyerReferralType(type=data)
            log.debug(f'adding to buyer_referral_type :: {buyer_referral_type.type}')
            db.session.add(buyer_referral_type)
            db.session.commit()

            log.debug(f'INSERT to buyer_referral_type Entity :: {repr(buyer_referral_type)}')
            return buyer_referral_type
        log.debug(f'buyer_type_referral already exists!')
        return None

#TODO: refactor Type domains
class CityDomain:
    """ Domain logic for city Entity """

    def transform_city(self, data: str) -> int:
        """ Transform incoming city_id to match DB schema """
        log.debug(f'transforming city :: {data}')

        mapping = {city.name: city.id for city in City.query.all()}
        log.debug(f'city mapping :: {mapping}')

        return mapping[data] if data in mapping else None

    def create_city(self, data):
        """ Create new city and post to DB """

        log.debug(f'checking if already exists in city :: parsed data :: {data}')
        data = data['name'].lower()

        city = City.query. \
            filter_by(name=data).first()

        log.debug(f'checking city :: {repr(city)}')

        if not city:
            city = City(name=data)
            # log.debug(f'adding to city Entity :: {buyer_referral_type.type}')
            log.debug(f'INSERT to city Entity :: {repr(city)}')
            db.session.add(city)
            db.session.commit()
            return city
        log.debug(f'city already exists!')
        return None

    def get_city(self, id: int):
        """ Returns city by id """
        result = City.query.get_or_404(id)
        log.debug(f'SELECT City by id :: {id}, {repr(result)}')
        return result


class EventDomain:
    """ Domain logic for buyer Entity """

    def create_event(self, data):
        """ Create new buyer and post to DB """

        # check if buyer_referral_type exists
        city_id = CityDomain().transform_city(data=['city_txt'])

        if city_id is None:
            CityDomain.create_city(data['city_txt'])

        event = Event(date=data['date'],
                      time=data['time'],
                      city_txt=data['city_txt'],
                      city_id=city_id)

        log.debug(f'INSERT to buyer Entity :: {repr(event)}')
        db.session.add(event)
        db.session.commit()
        return event

    def get_event(self, id: int):
        """ Returns event by id """

        result = Event.query.get_or_404(id)
        log.debug(f'SELECT Event by id :: {id}, {repr(result)}')
        return result

    def get_event_batch(self, city: str, date: datetime = None):
        """ Returns event by city, narrow down by date (optional) """

        # retrieve city id from city entity
        id = CityDomain.transform_city(city)

        if id:
            subquery = Event.query.filter_by(city_id=id)

            if subquery:
                if not date:
                    log.debug(f'SELECT event :: {repr(subquery)} by city :: {city} :: id :: {id}')
                    return subquery.all()

                current_date = datetime.utcnow().date()
                result = Event.query.filter(Event.date.between(date, current_date).in_(subquery))

                log.debug(f'SELECT event :: {repr(result)} by city :: {city} :: id :: {id} :: in dates :: {current_date} - {date}')
                return result
            log.debug(f'No events found for city :: {city} :: id :: {id}')
        else:
            log.debug(f'City has not been added yet!')
        return None

class TicketDomain:
    """ Domain logic for ticket Entity """

    def create_ticket(self, data):
        """ Create new ticket and post to DB """

        """ update event table """
        """ post to ticket table """

    def update_ticket(self, data):
        """ Update existing event when purchased """

        """ get event """

        """ update in db """

        """ return ticket """
        raise NotImplementedError

