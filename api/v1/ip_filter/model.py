from extensions import db
from flask import request
from functools import wraps
from sqlalchemy import text
from api.v1.ip_log.model import IpLogModel
from api.v1.activity_log.model import ActivityLogModel
import requests
import sys


class IpFilterModel(db.Model):
    __tablename__ = 'ip_filter'

    id = db.Column(db.Integer, primary_key = True)
    range1 = db.Column(db.String(15))
    range2 = db.Column(db.String(15))
    is_allowed = db.Column(db.Boolean)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def has_ip_access(cls, ip_address):
        #ip_allowed = cls.query.filter_by(ip_address = ip_address, is_allowed = True).all()
        #ip_denied = cls.query.filter_by(ip_address = ip_address, is_allowed = False).all()
        ip_allowed = cls.query.filter(text("INET_ATON(:ip_address) >= INET_ATON(range1) AND INET_ATON(:ip_address) <= INET_ATON(range2) AND is_allowed")).params(ip_address=ip_address).all()
        ip_denied = cls.query.filter(text("INET_ATON(:ip_address) >= INET_ATON(range1) AND INET_ATON(:ip_address) <= INET_ATON(range2) AND !is_allowed")).params(ip_address=ip_address).all()

        ip_temp = IpLogModel.query.filter_by(ip_address = ip_address).first()
        if ip_temp:
            ip_details = {
                'ip': ip_temp.ip_address,
                'country_name': ip_temp.country,
                'region_name': ip_temp.region,
                'city': ip_temp.city,
                'zip': ip_temp.zip,
                'latitude': ip_temp.latitude,
                'longitude': ip_temp.longitude
            }
        else:
            response = requests.get("http://api.ipstack.com/" + ip_address + "?access_key=e1b3c59e0ff04b4eadcede6d432e27bf")
            ip_details = response.json()

        ip_log = IpLogModel(
            ip_address = ip_details['ip'],
            country = ip_details['country_name'],
            region = ip_details['region_name'],
            city = ip_details['city'],
            zip = ip_details['zip'],
            latitude = ip_details['latitude'],
            longitude = ip_details['longitude']
        )

        ip_log.save_to_db()

        activity_log = ActivityLogModel(
            ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            route = request.url,
            jti = "",
            username = "",
            data = "{"+"}",
            remarks = "CHECK IP ACCESS"
        )
        activity_log.save_to_db()

        if ip_allowed and not ip_denied:
            return True
        else:
            return False


def ip_has_access(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        remote_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if IpFilterModel.has_ip_access(remote_address):
            return fn(*args, **kwargs)
        else:
            return {'message': 'Unauthorized IP address: ' + remote_address}, 403
    return wrapper
