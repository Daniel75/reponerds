# -*- coding: utf-8 -*-

from common import *

class Menu:

    def __init__(self, i, mode):
        self.item = {}
        self.mode = mode
        self.update_item(i)
        
    def update_item(self, i):
        self.item['mode']  = self.mode
        self.item['title'] = utfenc(i['title'])
        self.item['id']    = i['content_key']

        if i.get('icon', None):
            self.item['thumb'] = i['icon']