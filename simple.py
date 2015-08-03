__author__ = 'cameronlittle'

import datetime
import urlparse
import uuid

import bs4
import requests

from utils import unix_time_millis


"""
name=test%20title&target_amount=1000000&finish=1454083200000&image=goal-phone-bill.svg&color_name=purple&color=%239483AB&amount=1000000&archived=false&contributed_amount=0&created=1438556285037&locked=false&paused=false&seq=0&start=1438524000000&uuid=goal-919&category=&aprox_daily_contribution=5555.555555555556
"""
BASE_URL = "https://bank.simple.com"


def stringify(dct):
    new = dict.copy(dct)
    for key, val in dct.iteritems():
        if val is None:
            new[key] = ''
        elif val is False:
            new[key] = 'false'
        elif val is True:
            new[key] = 'true'
        else:
            new[key] = str(val)
    return new


class SimpleAccess(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.session = requests.Session()

        self.login()

    def _get_csrf(self, url):
        r = self.session.get(url)
        return bs4.BeautifulSoup(r.text, 'html.parser').find('meta', {'name': '_csrf'})['content']

    def login(self):
        url = urlparse.urljoin(BASE_URL, 'signin')
        csrf = self._get_csrf(url)

        r = self.session.post(url, data={
            'simple_username': self.username,
            'simple_password': self.password,
            '_csrf': csrf
        })
        if r.status_code / 500 == 5:
            raise Exception()
        # TODO: check for invalid auth

        return self

    def new_goal(self, name, target_amount, finish,
                 color_name='purple',
                 color='#9483AB',
                 start=None,
                 contributed_amount=0,
                 archived=False,
                 created=None,
                 locked=False,
                 paused=False,
                 seq=0,
                 uuid_=None,
                 category=None):
        if not isinstance(finish, datetime.datetime):
            raise ValueError()
        now = datetime.datetime.now()
        if start is None:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if created is None:
            created = now
        if uuid_ is None:
            uuid_ = uuid.uuid4()
        days_left = (finish - start).days
        daily_amount = (float(target_amount - contributed_amount) / days_left) * 10000
        target_amount *= 10000
        contributed_amount *= 10000
        data = stringify({
            "name":                 name,                       # test bill
            "target_amount":        target_amount,              # 1000000 == $100
            "finish":               unix_time_millis(finish),   # 1454169600000 == jan 30 2016
            "color_name":           color_name,                 # purple
            "color":                color,                      # #9483AB
            "amount":               target_amount,              # 1000000 == $100
            "archived":             archived,                   # false
            "contributed_amount":   contributed_amount,         # 0 ? target funding
            "created":              unix_time_millis(created),  # 1438559902579 ? now
            "locked":               locked,                     # false
            "paused":               paused,                     # false
            "seq":                  seq,                        # 0
            "start":                unix_time_millis(start),    # 1438524000000 ? today
            "uuid":                 uuid_,                 # goal-528
            "category":             category,
            "aprox_daily_contribution": daily_amount,           # 5524.861878453039 == 55 cents
            "initial_amount":       contributed_amount          # 200000 == $20
        })

        url = urlparse.urljoin(BASE_URL, 'goals')
        csrf = self._get_csrf(url)

        r = self.session.post(url, data=data, headers={
            'X-CSRF-Token': csrf,
            'X-Request': 'JSON',
            'Referer': url,
            'Origin': 'https://bank.simple.com',
        })
        if r.status_code / 500 == 5:
            raise Exception()

        return self
