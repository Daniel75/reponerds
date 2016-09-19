# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests
import json

site = 'vevo'
headers = {'User-Agent':'iPad','X-Requested-With': 'XMLHttpRequest'}

def get_videos(artist):
    videos = []
    token = get_token()
    artist_id = get_artist_id(artist,token)
    if artist_id:
        try:
            url = 'https://apiv2.vevo.com/artist/%s/videos' % str(artist_id)
            params = {'size':'200', 'page':'1', 'token':token}
            json_data = requests.get(url, headers=headers, params=params).json()
        except:
            return False
        try:
            for v in json_data['videos']:
                try:
                    id = v['isrc']
                    title = v['title']
                    image = v['thumbnailUrl']
                    duration = ''
                    try:
                        duration = v['duration']
                    except:
                        pass
                    if v['categories'][0] == 'Music Video':
                        videos.append({'site':site, 'artist':[artist], 'title':title, 'duration':duration, 'id':id, 'image':image})
                except:
                    pass
        except:
            pass
    elif artist_id == False:
        return False
    return videos
    
def get_video_url(id):
    video_url = None
    try:
        token = get_token()
        url = 'https://apiv2.vevo.com/video/%s/streams/mp4' % str(id)
        params = {'token':token}
        json_data = requests.get(url, headers=headers, params=params).json()
        for q in json_data:
            if q['quality'] == 'High':
                video_url = q['url']
                break
    except:
        pass
    return video_url

def get_artist_id(artist,token):
    artist_id = None
    try:
        url = 'https://apiv2.vevo.com/search'
        params = {'query':artist, 'includecategories':'music video', 'token':token}
        json_data = requests.get(url, headers=headers, params=params).json()
        artists = json_data['artists']
        for a in artists:
            if a['name'].encode('utf-8').lower() == artist.lower():
                artist_id = a['urlSafeName']
                break
    except:
        return False
    return artist_id

def get_token():
    token = None
    try:
        url = 'http://www.vevo.com/auth'
        json_data = requests.post(url, headers=headers).json()
        token = json_data['access_token']
    except:
        pass
    return token