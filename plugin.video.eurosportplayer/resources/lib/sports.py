# -*- coding: utf-8 -*-

from common import *

class Sports:

    def __init__(self, i):
        self.item          = {}
        self.item['mode']  = 'videos'
        self.item['title'] = utfenc(i['name'])
        self.item['id']    = i['id']
        self.item['thumb'] = self.thumb(i)
        
    def thumb(self, i):
        pictureurl = i['pictureurl'].replace(' ', '%20')
        if not pictureurl.startswith('http'):
            return image_base+pictureurl
        else:
            return pictureurl