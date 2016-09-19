# -*- coding: utf-8 -*-

import os,sys,urllib,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs

addon_id = 'plugin.video.sport1de'
addon = xbmcaddon.Addon()
home = addon.getAddonInfo('path').decode('utf-8')
iconimage = xbmc.translatePath(os.path.join(home, 'icon.png'))
pluginhandle = int(sys.argv[1])
datapath = xbmc.translatePath('special://profile/addon_data/%s' % addon_id).encode('utf-8')
cookie_file = os.path.join(datapath,'cookie.dat')
q = int(addon.getSetting('quality'))

from resources.lib.sport1 import Sport1
from resources.lib import helper
sport1 = Sport1()

def categories():
    items = helper.get_category_items()
    list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def tv_category():
    data = sport1.get_tv_epg()
    if data:
        items = helper.get_tv_items(data)
        list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def video_category():
    items = helper.get_video_category_items()
    list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def radio_category():
    items = helper.get_radio_category_items()
    list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def playlist():
    id = args['id'][0]
    data = sport1.get_page(id)
    if data:
        url = helper.get_playlist_url(data)
        if url:
            data = sport1.get_playlist(url)
            if data:
                items = helper.get_video_items(data,quality)
                list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def live_radio():
    data = sport1.get_radio()
    if data:
        items = helper.get_live_radio_items(data)
        list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def videos():
    id = args['id'][0]
    data = sport1.get_playlist(id)
    if data:
        items = helper.get_video_items(data,q)
        list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def livestream():
    data = sport1.get_tv()
    if data:
        items = helper.get_live_video_items(data)
        list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)
    
def play_video():
    path = args['id'][0]
    if path:
        listitem = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def play_tv():
    id = args['id'][0]
    data = sport1.get_tv(id,cookie_file)
    if data:
        result = helper.get_hls(data,q)
        if result:
            if '.m3u8' in result:
                delete_cookie()
                listitem = xbmcgui.ListItem(path=result)
                xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
            else:
                msg = result.replace(',',';')
                xbmc.executebuiltin(unicode('Notification(%s,%s,%d,%s)' % ('Info',msg,8000,iconimage)).encode('latin-1'))

def delete_cookie():
    try:
        cookie = xbmc.translatePath('special://temp/cookies.dat').encode('utf-8')
        if os.path.isfile(cookie):
            xbmcvfs.delete(cookie)
    except:
        pass
    
def list_items(items):
    for i in items:
        if i['type'] == 'dir':
            add_dir(i)
        elif i['type'] == 'video':
            add_video(i)

def add_dir(item):
    u = build_url({'mode':item['mode'], 'name':item['name'], 'id':item.get('id', '')})
    item=xbmcgui.ListItem(item['name'], iconImage="DefaultFolder.png", thumbnailImage=item.get('image', iconimage))
    xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=True)
    
def add_video(item):
    name = item['name']
    duration = item['duration']
    id = item['id']
    image = item.get('image', iconimage)
    plot = item['description']
    u = build_url({'mode': item['mode'], 'name':name, 'id':id})
    item=xbmcgui.ListItem(item['name'], iconImage="DefaultVideo.png", thumbnailImage=image)
    item.setInfo(type='Video', infoLabels={'Title':name, 'Plot':plot})
    item.addStreamInfo('video', {'duration':duration})
    item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item)

def build_url(query):
    return sys.argv[0] + '?' + urllib.urlencode(query)

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
xbmc.log('Arguments: '+str(args))

if mode==None:
    categories()
else:
    exec '%s()' % mode[0]