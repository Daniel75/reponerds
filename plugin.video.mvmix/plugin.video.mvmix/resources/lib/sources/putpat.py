# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests
import json

site = 'putpat'
base_url = 'http://www.putpat.tv/ws.json'
headers = {'User-Agent':'iPad','X-Requested-With': 'XMLHttpRequest'}

def get_videos(artist):
    videos = []
    artist_id = get_artist_id(artist)
    if artist_id:
        try:
            params = {'method':'Artist.assetsByArtistId', 'artistId':artist_id}
            json_data = requests.get(base_url, headers=headers, params=params).json()
        except:
            return False
        try:
            for item in json_data:
                try:
                    v = item['asset']
                    id = v['token']
                    artist = v['display_artist_title']
                    title = v['title']
                    image_id = str(v['video_file_id'])
                    image = ''
                    duration = ''
                    image = create_image_url(image_id)
                    try: duration = str(int(v['duration'])/25)
                    except: pass
                    if v['type'] == 'MusicVideo':
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
        params = {'method':'Asset.getClipForToken', 'token':id, 'streamingMethod':'http'}
        json_data = requests.get(base_url, headers=headers, params=params).json()
        clip = json_data[0]['clip']
        files = clip['tokens']
        for q in ['high','medium','low']:
            try: 
                video_url = files[q]
                video_url = check_file_type(video_url)
            except: 
                pass
            if video_url: break
    except:
        return False
    return video_url

def get_artist_id(artist):
    artist_id = None
    try:
        params = {'method':'Asset.quickbarSearch', 'searchterm':artist}
        json_data = requests.get(base_url, headers=headers, params=params).json()
        artists = json_data['quickbar_search']['artists']
        for a in artists:
            if a['title'].encode('utf-8').lower() == artist.lower():
                artist_id = str(a['id'])
    except:
        pass
    return artist_id
    
def create_image_url(id):
    # http://files.putpat.tv/artwork/posterframes/00538/0053825/v0053825_posterframe_putpat_large.jpg
    import string
    _id_2 = string.zfill(id, 7)
    _id_1 = _id_2[0:5]
    image_url = 'http://files.putpat.tv/artwork/posterframes/%s/%s/v%s_posterframe_putpat_large.jpg' % (_id_1,_id_2,_id_2)
    return image_url
    
def check_file_type(url):
    try:
        r = requests.head(url)
        type = r.headers.get('content-type')
        if type == 'video/mp4' or type == 'video/x-flv' or type == 'application/octet-stream' or type == 'application/x-mpegurl':
            return url
    except:
        pass