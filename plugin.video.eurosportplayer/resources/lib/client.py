# -*- coding: utf-8 -*-

import simple_requests as requests
from common import *

class Client(object):

    def __init__(self):
        
        VS_URL  = 'http://videoshop.ext.eurosport.com/JsonProductService.svc/'
        CRM_URL = 'https://playercrm.ssl.eurosport.com/JsonPlayerCrmApi.svc/'
        
        self.CRM_LOGIN      = CRM_URL + 'Login'
        self.VIDEO_PRODUCTS = VS_URL  + 'GetAllProductsByDeviceMobile'
        self.VIDEO_CATCHUPS = VS_URL  + 'GetAllCatchupCache'
        self.VIDEO_TOKEN    = VS_URL  + 'GetToken'

        self.headers    = {
                            'User-Agent':'iPhone',
                            'Referer':base_url
                            }
                            
        self.login_data = {
                            'email':'', 
                            'password':'', 
                            'udid':'00000000-0000-0000-0000-000000000000'
                            }
                            
        self.context    = {
                            'g':'', 
                            'd':'2', 
                            's':'1', 
                            'p':'1',
                            'b':'apple'
                            }
                            
        self.dvs        = {
                            'userid':'', 
                            'hkey':'', 
                            'languageid':'', 
                            'isbroadcasted':'1', 
                            'isfullaccess':'0'
                            }
        
        self.set_user_data()
        
    def set_user_data(self):
        self.set_location()
        self.login_data['email']    = utfenc(email)
        self.login_data['password'] = utfenc(password)
        self.dvs['userid']          = userid
        self.dvs['hkey']            = hkey

    def set_location(self):
        data = self.get_data(base_url)
        c = re.search("crmlanguageid\s*:\s*'(\d+)'", data)
        if c:
            self.dvs['languageid'] = c.group(1)
        g = re.search("geoloc\s*:\s*'(\w+)'", data)
        if g:
            self.context['g'] = g.group(1)
        log('[eurosportplayer] geolocation: %s' % (self.context['g']))

    def set_user_ref(self):
        user_ref = self.ep_login()
        if user_ref.get('Response', None):
            log('[eurosportplayer] login: %s' % (utfenc(user_ref['Response']['Message'])))
        if user_ref.get('Id', '') and user_ref.get('Hkey', ''):
            self.dvs['userid'] = user_ref['Id']
            addon.setSetting('userid', user_ref['Id'])
            self.dvs['hkey']   = user_ref['Hkey']
            addon.setSetting('hkey', user_ref['Hkey'])
    
    def products(self):
    
        def get_url():
            encoded = urllib.urlencode({'data':json.dumps(self.dvs), 'context':json.dumps(self.context)})
            return self.VIDEO_PRODUCTS + '?' + encoded
        
        data = self.json_request(get_url())
        if not self.logged_in(data):
            self.set_user_ref()
            data = self.json_request(get_url())
        return data

    def catchups(self):
        encoded = urllib.urlencode({'data':json.dumps(self.dvs), 'context':json.dumps(self.context)})
        url     = self.VIDEO_CATCHUPS + '?' + encoded
        return self.json_request(url)
        
    def ep_login(self):
        encoded = urllib.urlencode({'data':json.dumps(self.login_data), 'context':json.dumps(self.context)})
        url     = self.CRM_LOGIN + '?' + encoded
        return self.json_request(url)
        
    def logged_in(self, data):
        if data.get('ActiveUserRef', None):
            if 'success' in data['ActiveUserRef']['Response']['Message']:
                return True
            else:
                log('[eurosportplayer] error: %s' % (utfenc(data['ActiveUserRef']['Response']['Message'])))
        return False
        
    def token(self):
        encoded  = urllib.urlencode({'data':json.dumps(self.dvs), 'context':json.dumps(self.context)})
        tokenUrl = self.VIDEO_TOKEN + '?' + encoded
        r = requests.get(tokenUrl, headers=self.headers)
        if r.headers.get('content-type', '').startswith('application/json'):
            return r.json()
        else:
            return {}
        
    def get_data(self, url):
        r = requests.get(url, headers=self.headers, allow_redirects=True)
        if r:
            return r.text
        else:
            return ''
            
    def json_request(self, url):
        r = requests.get(url, headers=self.headers)
        if r.headers.get('content-type', '').startswith('application/json'):
            return r.json()
        else:
            log('[eurosportplayer] error: json request failed with %s response' % (str(r.status_code)))
            return {}