# -*- coding: utf-8 -*-

import simple_requests as requests
from common import *

class Client(object):

    def __init__(self):
    
        self.headers      = {
                            'User-Agent':  'Kodi',
                            'Referer'   :  'http://www.laola1.tv'
                            }
                            
        self.params       = {}
        self.post_data    = {}
                            
        self.v2           = 'https://club.laola1.tv/sp/laola1tv/api/v2/'
        self.v3           = 'https://club.laola1.tv/sp/laola1tv/api/v3/'
        self.feed         = 'http://www.laola1.tv/feed/'
        
        self.partner      = '22'
        self.target       = '8'
        self.target_vod   = '2'
        self.target_live  = '17'

    def content(self, type):
        self.params = {
                        'type':type,
                        'target':self.target,
                        'customer':'1001',
                        'lang':lang,
                        'portal':portal
                        }
        return self.json_request(self.feed + 'appfeed.php')
        
    def videos(self, id):
        self.params = {
                        'targetID':self.target,
                        'template':'3',
                        'v':'2',
                        'partner':self.partner,
                        'stageID':id,
                        'page':'0',
                        'rows':'50',
                        'lang':lang,
                        'portal':portal,
                        'format':'json'
                        }
        return self.json_request(self.feed + 'app_video.feed.php')
        
    def live_feed(self):
        self.params = {
                        'targetID':self.target_live,
                        'order':'asc',
                        'partner':self.partner,
                        'lang':lang,
                        'geo':portal,
                        'records':'50',
                        'format':'json'
                        }
        return self.json_request(self.feed + 'app_video.feed.php')
            
    def player(self, id, params):
        if params == 'true':
            target = self.target_live
        else:
            target = self.target_vod
            
        self.headers.update({'cookie':cookie})
        
        self.post_data = {
                            '0' : 'tv.laola1.laolatv.premiumclub',
                            '1': 'tv.laola1.laolatv.premiumclub_all_access'
                            }
                            
        self.params    = {
                            'videoId': id,
                            'label' : 'laola1tv',
                            'area'  : 'laola1tv',
                            'target': target
                            }
        return self.json_request(self.v3 + 'user/session/premium/player/stream-access')
            
    def unas_xml(self,id):
        r   = requests.get(id + '&format=iphone', headers=self.headers)
        if r:
            return r.text
        else:
            return ''
        
    def login(self):
        data = {
                'e': utfenc(email),
                'p': utfenc(password)
                }
        r = requests.post(self.v2 + 'session', headers=self.headers, data=data)
        return r.headers.get('set-cookie', '')
        
    def logout(self):
        if cookie:
            self.headers['cookie'] = cookie
            r = requests.post(self.v2 + 'session/delete', headers=self.headers)
            
    def deletesession(self):
        if cookie:
            self.headers['cookie'] = cookie
            r = requests.post(self.v3 + 'user/session/premium/delete', headers=self.headers)

    def user(self, _cookie_):
        self.headers['cookie'] = _cookie_
        return self.json_request(self.v2 + 'user')
        
    def json_request(self, url):
        if self.post_data:
            r = requests.post(url, headers=self.headers, data=self.post_data, params=self.params)
        else:
            r = requests.get(url, headers=self.headers, params=self.params)
        if r.headers.get('content-type', '').startswith('application/json'):
            return r.json()
        else:
            log('[laola1tv] error: json request failed with %s response' % (str(r.status_code)))
            return {}