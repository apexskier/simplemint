__author__ = 'cameronlittle'

import urlparse

import bs4
import requests


BASE_URL = 'https://wwws.mint.com'


class MintAccess(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.session = requests.Session()

        self.login()

    def login(self):
        """
        curl 'https://wwws.mint.com/loginUserSubmit.xevent'
            -H 'Cookie:
                mp_dc5a4918b7ee39a4d1b73c7f323457ef_mixpanel=%7B%22distinct_id%22%3A%20%2214ef3e6a1c376-04d686302-34627b06-fa000-14ef3e6a1c410e%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D;
                _exp_mintPN=1;
                MINTJSESSIONID=EB315AE46F7707CF9C6775D185C7DB8A;
                ROUTEID=.zORQ/lPg;
                s_fid=2A1C03ADA43C0CC5-12D2233C20DBD527;
                source=source;
                __mintMoment_CK=;
                s_cc=true;
                s_sq=%5B%5BB%5D%5D;
                mintPN=2'
            -H 'Origin: https://wwws.mint.com'
            -H 'Accept-Encoding: gzip, deflate'
            -H 'Accept-Language: en-US,en;q=0.8'
            -H 'Upgrade-Insecure-Requests: 1'
            -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
            -H 'Content-Type: application/x-www-form-urlencoded'
            -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            -H 'Cache-Control: max-age=0'
            -H 'Referer: https://wwws.mint.com/loginJumper.event'
            -H 'Connection: keep-alive'
            --data '
                validation=&
                simple_username=***********&
                simple_password=********&
                task=L&
                timezone=&
                nextPage=&
                browser=&
                browserVersion=&
                os='
        """
        url = urlparse.urljoin(BASE_URL, 'loginUserSubmit.xevent')
        headers = {
            'Origin': 'https://wwws.mint.com',
            'Referer': 'https://wwws.mint.com/loginJumper.event'
        }
        data = {
            'simple_username': self.username,
            'simple_password': self.password,
            'task': 'L'
        }

        r = self.session.post(url, data=data, headers=headers)
        if r.status_code / 500 == 5:
            raise Exception()

        return self
