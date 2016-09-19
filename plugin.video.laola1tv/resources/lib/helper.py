# -*- coding: utf-8 -*-

from common import *
    
def stageid(data,ck):
    content = data['content']
    contentPage = str(content[ck]['contentPage'])
    r = re.search("u'stageid': u'(\d+)'", contentPage)
    if r:
        return r.group(1)

def unas_url(data):
    if data.get('status', 'error') == 'success':
        return data['data']['stream-access'][0]
    else:
        message = data.get('message', 'error')
        dialog.ok('Laola1 TV', utfenc(message))
        
def user(data):
    if data.get('error', None):
        return data['error'][0]
    elif data.get('result', None):
        return 'country=%s premium=%s' % (data['result']['country'], data['result']['premium'])

def master(data):
    y = ['350','750','1000','1500','6000']
    z = y[int(quality)]
    a = re.search('auth="(.*?)"', data)
    b = re.search('url="(http.*?)"', data)
    c = re.search('comment="(.*?)"', data)
    if a and b:
        return '%s?hdnea=%s&b=0-%s' % (b.group(1), a.group(1), z)
    elif c:
        dialog.ok('Laola1 TV', utfenc(c.group(1)))

def create_cookie(data):
    cookie = ''
    premium = re.search('premium=(.*?);', data)
    email   = re.search('email=(.*?);', data)
    session = re.search('session=(.*?);', data)
    if premium and email and session:
        cookie = 'premium=%s; email=%s; session=%s' % (premium.group(1),email.group(1),session.group(1))
    return cookie