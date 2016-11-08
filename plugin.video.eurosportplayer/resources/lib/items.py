# -*- coding: utf-8 -*-

from common import *

class Items:

    def __init__(self):
        self.cache = True
        self.video = False
    
    def list(self):
        if self.video:
            xbmcplugin.setContent(addon_handle, content)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=self.cache)
        
        if force_view:
            xbmc.executebuiltin('Container.SetViewMode(%s)' % view_id)

    def add(self, item):    
        data = {
                'mode'   : item['mode'],
                'title'  : item['title'],
                'id'     : item.get('id', ''),
                'params' : item.get('params', '')
                }
                    
        art = {
                'thumb'  : item.get('thumb', icon),
                'poster' : item.get('thumb', icon),
                'fanart' : fanart
                }
                
        labels = {
                    'title'     : item['title'],
                    'plot'      : item.get('plot', ''),
                    'premiered' : item.get('date', ''),
                    'episode'   : item.get('episode', 0)
                    }
        
        listitem = xbmcgui.ListItem(item['title'])
        listitem.setArt(art)
        listitem.setInfo(type='Video', infoLabels=labels)
        
        if 'play' in item['mode']:
            self.cache = False
            self.video = True
            folder = False
            listitem.addStreamInfo('video', {'duration':item.get('duration', 0)})
            listitem.setProperty('IsPlayable', 'true')
        else:
            folder = True
            
        xbmcplugin.addDirectoryItem(addon_handle, build_url(data), listitem, folder)
        
    def play(self, path):
        listitem = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem)
        
items = Items()

def channel(data):
    from channels import Channels
    obj = data.get('PlayerObj', [])
    for i in obj:
        items.add(Channels(i).item)
    items.add({'mode':'sports', 'title':getString(30101), 'plot':getString(30102)})
    items.list()

def sport(data):
    from sports import Sports
    sports = data.get('PlayerObj', {'sports': []})['sports']
    for i in sports:
        items.add(Sports(i).item)
    items.list()
    
def video(data, match):
    from catchups import Catchups
    catchups = data.get('PlayerObj', {'catchups': []})['catchups']
    for i in catchups:
        if str(match) == str(i['sport']['id']):
            items.add(Catchups(i).item)
    items.list()
    
def play(path):
    items.play(path)