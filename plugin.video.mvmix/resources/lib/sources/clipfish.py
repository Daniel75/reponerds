# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests
import json, re

site = 'clipfish'

def get_videos(artist):
    videos = []
    q = re.sub('[^\s0-9a-zA-Z]+', '', artist)
    url = 'http://www.clipfish.de/devmobileapp/searchvideos/%s/mostrecent/1/100' % q
    try:
        json_data = requests.get(url).json()
    except:
        return False
    try:
        result = json_data['videos']
        for r in result:
            try:
                t = r['title']
                match = t.split(' - ')
                name = match[0].strip()
                if name.encode('utf-8').lower() == artist.lower():
                    title = match[1]
                    if len(match) > 2:
                        try: title = title+match[2]
                        except: pass
                    id = r['video_url_wifi_quality']
                    image = r['media_thumbnail']
                    duration = 0
                    try: duration = r['media_length']
                    except: pass
                    if int(duration) > 150:
                        videos.insert(0, {'site':site, 'artist':[name], 'title':title, 'duration':duration, 'id':id, 'image':image})
            except:
                pass
    except:
        pass
    return videos
    
def get_video_url(id):
    return id