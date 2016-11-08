# -*- coding: utf-8 -*-

from common import *

def token(data):
    if data.get('PlayerObj', ''):
        return data['PlayerObj']['token']

def index(data):
    y = [600000,1200000,2400000,4800000]
    z = y[int(quality)]
    result = None
    list = []
    pattern = 'bandwidth=(\d+).*?\n(http.*?)$'
    match = re.findall(pattern, data, re.I|re.M)
    for b,u in match:
        list.append({'bandwidth':int(b), 'url':u})
    if list:
        list = sorted(list, key=lambda k:k['bandwidth'])
        for x in list:
            if x['bandwidth'] < z:
                index = x['url']
            else:
                break
        return index
    return result
    
def add_param(url,param):
    if '?' in url:
        url = '%s&%s' % (url,param)
    else:
        url = '%s?%s' % (url,param)
    return url