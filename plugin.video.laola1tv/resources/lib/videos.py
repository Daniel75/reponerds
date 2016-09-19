# -*- coding: utf-8 -*-

from common import *

class Videos:

    def __init__(self, i):
        self.item  = {}
        self.a     = i['@attributes']
        self.start = self.a['scheduled_start'][:16]
        self.update_item(i)
          
    def update_item(self, i):
        self.item['mode']     = 'play'
        self.item['params']   = 'false'
        self.item['title']    = utfenc(i['TITLE'])
        self.item['id']       = self.a['ID']
        self.item['plot']     = utfenc(i['DESCRIPTION'])
        self.item['date']     = self.start[:10]
        self.item['thumb']    = i['IMAGE_ORIGINAL']