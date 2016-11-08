# -*- coding: utf-8 -*-

from common import *

class Catchups:

    def __init__(self, i):
        self.item = {}
        self.item['mode']     = 'play'
        self.item['title']    = utfenc(i['titlecatchup'].strip())
        self.item['id']       = i['catchupstreams'][0]['url']
        self.item['duration'] = i['durationInSeconds']
        self.item['plot']     = utfenc(i['description'])
        self.item['thumb']    = i['pictureurl']+'|User-Agent=Android'
        self.item['episode']  = i['idcatchup']
        self.item['date']     = i['startdate']['technicaldate']