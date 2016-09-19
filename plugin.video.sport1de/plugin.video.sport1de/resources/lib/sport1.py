# -*- coding: utf-8 -*-

import xbmc,xbmcaddon,xbmcvfs
import re,requests
addon = xbmcaddon.Addon()

class Sport1(object):

    def __init__(self):
        self.headers = {'User-Agent':  'iPhone',
                        'Referer'   :  'http://video.sport1.de',
                        'Host'      :  'video.sport1.de'}
        self.cookies = None

    def get_playlist(self,id):
        result = {}
        try:
            url = 'http://video.sport1.de/api/playlist/%s' % (id)
            data = requests.get(url, headers=self.headers).json()
            return data
        except:
            pass
        return result

    def get_video(self,id):
        result = {}
        try:
            url = 'http://video.sport1.de/api/video/%s' % (id)
            data = requests.get(url, headers=self.headers).json()
            return data
        except:
            pass
        return result

    def get_tv_epg(self):
        result = {}
        try:
            url = 'http://video.sport1.de/api/epg/tv'
            data = requests.get(url, headers=self.headers).json()
            return data
        except:
            pass
        return result

    def get_fm_epg(self):
        result = {}
        try:
            url = 'http://video.sport1.de/api/epg/fm'
            data = requests.get(url, headers=self.headers).json()
            return data
        except:
            pass
        return result
        
    def get_tv(self,url=False,cookie_file=False):
        result = None
        
        self.headers.update({   'Referer'   :  'http://tv.sport1.de',
                                'Host'      :  'tv.sport1.de'})
        
        if url:
            if not '/sport1/' in url:
                if not self.logged_in(cookie_file):
                    self.login(cookie_file)
        else:
            url = 'http://tv.sport1.de/mobile/'
        
        if self.cookies:
            self.headers.update({'cookie':self.cookies})
        
        try:
            data = requests.get(url, headers=self.headers).text
            return data
        except:
            pass
        return result

    def get_radio(self):
        result = None
        try:
            url = self.get_date()
            self.headers.update({   'Referer'   :  'http://sportsapi.sport1.de',
                                    'Host'      :  'sportsapi.sport1.de'})
            data = requests.get(url, headers=self.headers).json()
            return data
        except:
            pass
        return result

    def login(self,cookie_file):
        email = addon.getSetting('email').encode('utf-8')
        password = addon.getSetting('password').encode('utf-8')
        if email and password:
            data = {'log_email'             :  email,
                    'log_pw'                :  password,
                    'log_goback'            :  '0',
                    'log_persistence_cookie':  '1'}
            url = 'https://tv.sport1.de/mobile/home/index.php'
            try:
                r = requests.post(url, headers=self.headers, data=data)
                if '<div class="logged-in">' in r.text:
                    self.cookies = r.headers['set-cookie']
                    self.save_cookie(cookie_file)
                else:
                    pattern = '<span class="loginError.*?">(.*?)</span>'
                    s = re.search(pattern, r.text)
                    if s:
                        msg = s.group(1)
                    else:
                        msg = 'Login Fehlgeschlagen'
                    xbmc.executebuiltin(unicode('Notification(%s,%d)' % (msg,8000)).encode('utf-8'))
            except:
                pass

    def logged_in(self,cookie_file):
        result = False
        try:
            if xbmcvfs.exists(cookie_file):
                f = xbmcvfs.File(cookie_file)
                cookie = f.read()
                f.close()
                url = 'https://tv.sport1.de/mobile/home/index.php'
                self.headers.update({'cookie':cookie})
                text = requests.get(url, headers=self.headers).text
                if '<div class="logged-in">' in text:
                    self.cookies = cookie
                    return True
        except:
            pass
        return result

    def save_cookie(self, cookie_file):
        f = xbmcvfs.File(cookie_file, 'w')
        result = f.write(self.cookies)
        f.close()

    def get_date(self):
        result = None
        try:
            url = 'http://www.sport1.de/api/pages/465'
            data = requests.get(url, headers=self.headers).json()
            u = data['elements'][0]['elements'][0]['url']
            return u
        except:
            pass
        return result