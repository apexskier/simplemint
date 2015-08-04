__author__ = 'cameronlittle'

import urlparse
import json
import HTMLParser

import bs4
import requests


BASE_URL = 'https://wwws.mint.com'


class AuthenticationError(Exception):
    pass


class MintAccess(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._categories = None

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

        r = self.session.post(url, data={
            'simple_username': self.username,
            'simple_password': self.password,
            'task': 'L'
        }, headers={
            'Origin': 'https://wwws.mint.com',
            'Referer': 'https://wwws.mint.com/loginJumper.event'
        })
        if r.status_code / 500 == 5:
            raise Exception()
        html = bs4.BeautifulSoup(r.text)
        error = html.find('input', attrs={"id": "failedAuthenticationData"})
        if error:
            reason = json.loads(HTMLParser.HTMLParser().unescape(error['value']))
            reason['error'] = json.loads(reason['error']['vError'])
            raise AuthenticationError(reason['error']['copy'])

        return self

    @property
    def categories(self):
        """
        'https://wwws.mint.com/app/getJsonData.xevent?task=categories&rnd=1438658432396'
        -H 'Cookie: mp_dc5a4918b7ee39a4d1b73c7f323457ef_mixpanel=%7B%22distinct_id%22%3A%20%2214ef6b80ccb76-0bf94436a-17396a55-1aeaa0-14ef6b80ccc521%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; __mintMoment_CK=; mintPN=2; _exp_mintPN=2; MINTJSESSIONID=9E92B86514999E4023A382A07C81262E; currentClientType=Mint; brandingOption=whitelabel; current-config-source=Back-end; qbn.ptc.authid=812122250; AUTH_ID=812122250; qbn.ptc.ticket=V1-110-Q01l3ffujdduegysjy7v4k; IAM_TICKET=V1-110-Q01l3ffujdduegysjy7v4k; mu=1; userguid=5E9968B64CE115D7; mintUserName="cameron@camlittle.com"; ROUTEID=.LARjMMJd; wa_login=08%2F16%2F2010%2009%3A25%20PM%2C08%2F03%2F2015%2007%3A29%20PM%2C08%2F03%2F2015%2008%3A19%20PM%2C%2C4%2C%2C%2C%2C%2Cau%2C%2C%2C5E9968B64CE115D7; _ga=GA1.2.1612793266.1438658358; _gat=1; mbox=check#true#1438658457|session#1438658354665-630645#1438660257|PC#1438658354665-630645.20_15#1441250397; s_cc=true; s_fid=2CE740778B490721-12AF7CCA73A5EFCE; s_sq=%5B%5BB%5D%5D'
        -H 'X-NewRelic-ID: UA4OVVFWGwYJV1FTBAE='
        -H 'Accept-Encoding: gzip, deflate, sdch'
        -H 'Accept-Language: en-US,en;q=0.8'
        -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
        -H 'Accept: */*'
        -H 'Referer: https://wwws.mint.com/planning.event'
        -H 'X-Requested-With: XMLHttpRequest'
        -H 'Connection: keep-alive'
        """
        if self._categories is None:
            url = urlparse.urljoin(BASE_URL, 'getJsonData.xevent')
            r = self.session.post(url, params={
                'task': 'categories'
            }, headers={
                'Referer': 'https://wwws.mint.com/planning.event'
            })
            if r.status_code / 500 == 5:
                raise Exception()
            self._categories = r.json()
        return self._categories
