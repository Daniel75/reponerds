# -*- coding: utf-8 -*-

import json,os,re,sys,urllib,urlparse
import time,datetime
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs

addon_id     = 'plugin.video.eurosportplayer'
addon_handle = int(sys.argv[1])
addon        = xbmcaddon.Addon()
dialog       = xbmcgui.Dialog()
icon         = addon.getAddonInfo('icon')
fanart       = addon.getAddonInfo('fanart')
force_view   = addon.getSetting('force_view') == 'true'
content      = addon.getSetting('content')
view_id      = addon.getSetting('view_id')
email        = addon.getSetting('email')
password     = addon.getSetting('password')
userid       = addon.getSetting('userid')
hkey         = addon.getSetting('hkey')
quality      = addon.getSetting('quality')

base_url     = 'http://www.eurosportplayer.com'
image_base   = 'http://i.eurosportplayer.com/'

def log(msg):
    xbmc.log(str(msg), xbmc.LOGNOTICE)
    
def getString(id):
    return utfenc(addon.getLocalizedString(id))

def build_url(query):
    return sys.argv[0] + '?' + urllib.urlencode(query)
    
def utfenc(str):
    try:
        str = str.encode('utf-8')
    except:
        pass
    return str

def clearString(str):
    try:
        str = re.sub('\(  .+?\)$|<.+?>|wifi tablet ios|none', '', str, flags=re.I)
    except:
        pass
    return str

def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6