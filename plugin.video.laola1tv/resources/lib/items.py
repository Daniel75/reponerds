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

def menu(data):
    from menu import Menu
    items.add({'mode':'live', 'title':getString(30101)})
    if data.get('menu_items', None):
        channels = data['menu_items'][5]['Sport Channel']
        for i in channels:
            items.add(Menu(i, 'sub_menu').item)
    items.list()
    
def sub_menu(data,channel):
    from menu import Menu
    channels = data['menu_items'][5]['Sport Channel']
    for c in channels:
        if channel == utfenc(c['title']):
            for i in c['submenu']:
                items.add(Menu(i, 'videos').item)
            break
    items.list()

def live(data):
    from live import Live
    videos = data.get('video', [])
    for i in videos:
        items.add(Live(i).item)
    items.list()

def video(data):
    from videos import Videos
    videos = data.get('VIDEO', [])
    for i in videos:
        items.add(Videos(i).item)
    items.list()
    
def play(path):
    items.play(path)