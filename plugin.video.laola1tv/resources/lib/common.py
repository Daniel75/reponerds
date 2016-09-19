# -*- coding: utf-8 -*-

import json,os,re,sys,urllib,urlparse
import time,datetime
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs

addon_id     = 'plugin.video.laola1tv'
addon_handle = int(sys.argv[1])
addon        = xbmcaddon.Addon()
dialog       = xbmcgui.Dialog()
icon         = addon.getAddonInfo('icon')
fanart       = addon.getAddonInfo('fanart')
force_view   = addon.getSetting('force_view') == 'true'
content      = addon.getSetting('content')
view_id      = addon.getSetting('view_id')
quality      = addon.getSetting('quality')

email        = addon.getSetting('email')
password     = addon.getSetting('password')
cookie       = addon.getSetting('cookie')
languages    = ['de','en','ru']
portals      = ['at','de','int','ru','cis']
portal       = portals[int(addon.getSetting('portal'))]
lang         = languages[int(addon.getSetting('lang'))]

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

def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6