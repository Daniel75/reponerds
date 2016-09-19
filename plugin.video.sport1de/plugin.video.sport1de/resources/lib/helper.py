# -*- coding: utf-8 -*-

import re

def get_category_items():
    items = [
                {'type':'dir', 'mode':'tv_category', 'name':'TV'},
                {'type':'dir', 'mode':'video_category', 'name':'Videos'},
                {'type':'dir', 'mode':'radio_category', 'name':'Radio'},
            ]
    return items

def get_video_category_items():
    items = [
                {'type':'dir', 'mode':'videos', 'id':'0_nqmdcpgb', 'name':'Neueste Videos'},
                {'type':'dir', 'mode':'videos', 'id':'0_y8s3i6xf', 'name':'Top Videos'},
                {'type':'dir', 'mode':'videos', 'id':'0_ppyiwf4n', 'name':'News'},
                {'type':'dir', 'mode':'videos', 'id':'0_a9zu407t', 'name':'Fussball'},
                {'type':'dir', 'mode':'videos', 'id':'0_jaacx0hz', 'name':'Bundesliga Aktuell'},
                {'type':'dir', 'mode':'videos', 'id':'0_8y23jpga', 'name':'Regionalliga'},
                {'type':'dir', 'mode':'videos', 'id':'0_uhhrbozp', 'name':'UEFA Europa League'},
                {'type':'dir', 'mode':'videos', 'id':'0_wich8xsf', 'name':'Fussball International'},
                {'type':'dir', 'mode':'videos', 'id':'0_7mp3uktl', 'name':'Doppelpass'},
                {'type':'dir', 'mode':'videos', 'id':'0_mo2ihu8w', 'name':'Basketball'},
                {'type':'dir', 'mode':'videos', 'id':'0_019rh7kw', 'name':'Basketball Euroleague'},
                {'type':'dir', 'mode':'videos', 'id':'0_pn8mczrd', 'name':'Basketball Beko BBL'},
                {'type':'dir', 'mode':'videos', 'id':'0_icmwhaja', 'name':'Handball'},
                {'type':'dir', 'mode':'videos', 'id':'0_gk0pip9o', 'name':'Volleyball'},
                {'type':'dir', 'mode':'videos', 'id':'0_q4hdin4o', 'name':'Tennis'},
                {'type':'dir', 'mode':'videos', 'id':'0_jf75kubn', 'name':'Eishockey'},
                {'type':'dir', 'mode':'videos', 'id':'0_u40ck8u8', 'name':'Hockey'},
                {'type':'dir', 'mode':'videos', 'id':'0_gsten8d4', 'name':'Poker'},
                {'type':'dir', 'mode':'videos', 'id':'0_qi2uk5y3', 'name':'Europaspiele'},
                {'type':'dir', 'mode':'videos', 'id':'0_a9z7y19x', 'name':'NBA'},
                {'type':'dir', 'mode':'videos', 'id':'0_z0gb3mxb', 'name':'NBA Playoff Moments'},
                {'type':'dir', 'mode':'videos', 'id':'0_9227gzr8', 'name':'NFL'},
                {'type':'dir', 'mode':'videos', 'id':'0_c6ebz286', 'name':'NHL'},
                {'type':'dir', 'mode':'videos', 'id':'0_db3anfk2', 'name':'Darts'},
                {'type':'dir', 'mode':'videos', 'id':'0_muvilawb', 'name':'Darts Premier League'},
                {'type':'dir', 'mode':'videos', 'id':'0_i4pge47z', 'name':'Motorsport Top Videos'},
                {'type':'dir', 'mode':'videos', 'id':'0_z5fy2g2b', 'name':'Formel1'},
                {'type':'dir', 'mode':'videos', 'id':'0_45uc5875', 'name':'DTM'},
                {'type':'dir', 'mode':'videos', 'id':'0_jm2vmjdv', 'name':'WRC'},
                {'type':'dir', 'mode':'videos', 'id':'0_zbiw72l8', 'name':'VLN'},
                {'type':'dir', 'mode':'videos', 'id':'0_nzv2abib', 'name':'ADAC Formel 4'},
                {'type':'dir', 'mode':'videos', 'id':'0_jcfvj2uk', 'name':'ADAC GT Masters'},
                {'type':'dir', 'mode':'videos', 'id':'0_5z28uf65', 'name':'Boulevard'},
                {'type':'dir', 'mode':'videos', 'id':'0_lz5w9zcl', 'name':'Die PS Profis'},
                {'type':'dir', 'mode':'videos', 'id':'0_xzi6ed9c', 'name':'Turbo'},
                {'type':'dir', 'mode':'videos', 'id':'0_t09zsmy7', 'name':'Auftrag Auto'},
                {'type':'dir', 'mode':'videos', 'id':'0_1u6iputx', 'name':'Nine Knights'},
                {'type':'dir', 'mode':'videos', 'id':'0_gmq99ilw', 'name':'Clipmasters'},
                {'type':'dir', 'mode':'videos', 'id':'0_6l0tihks', 'name':'Specials'},
            ]
    return items

def get_radio_category_items():
    items = [   
                {'type':'dir', 'mode':'live_radio', 'name':'Live'},
                {'type':'dir', 'mode':'videos', 'id':'0_nv1vov1f', 'name':'Radio Highlights'},
                {'type':'dir', 'mode':'videos', 'id':'0_h2dnj27a', 'name':'Podcast'},
                {'type':'dir', 'mode':'videos', 'id':'0_ev7ho53z', 'name':'Bundesliga'},
                {'type':'dir', 'mode':'videos', 'id':'0_3kjxbpjs', 'name':'2. Bundesliga'},
                {'type':'dir', 'mode':'videos', 'id':'0_r3t0uc0f', 'name':'Europa League'},
                {'type':'dir', 'mode':'videos', 'id':'0_36tbfldi', 'name':'DFB-Pokal'},
                {'type':'dir', 'mode':'videos', 'id':'0_qol6tqkd', 'name':'DFB-Team'},
                {'type':'dir', 'mode':'videos', 'id':'0_4g0s69pv', 'name':'Doppelpass'}
            ]
    return items

def get_playlist_url(data):
    url = None
    elements = data['elements']
    for i in elements:
        sub_elements = i.get('elements', '')
        if sub_elements:
            for s in sub_elements:
                type = s.get('type', '')
                if type == 'video_detailed_band':
                    url = s['elements'][0]['url']
                    break
    return url

def get_video_items(data,q):
    from datetime import datetime
    y = ['low_quality','mid_quality','high_quality']
    z = y[q]
    items = []
    videos = data['videos']
    for i in videos:
        title = i['title']
        image = i['image']
        id = i['id']
        description = i['description'].encode('utf-8')
        a = image.split(id)[0]
        image = '%s%s/width/400' % (a,id)
        duration = int(i['durationSeconds'])
        date = i['date']
        dt = datetime.fromtimestamp(int(date))
        dt = str(dt)[:16]
        name = '%s (%s)' % (title,dt)
        name = name.encode('utf-8')
        url = i['url']
        for u in url:
            mp4 = url[u]
            if z == u:
                break
        items.append({'type':'video', 'mode':'play_video', 'name':name, 'id':mp4, 'description':description, 'image':image, 'duration':duration})
    return items

def get_tv_items(data):
    items = []
    stations = data['stations']
    for s in stations:
        title = s['title']
        current_programs = s['current_programs'][0]
        description = current_programs['description']
        start = current_programs['from'].split('T')[-1]
        end = current_programs['to'].split('T')[-1]
        link = s['link']
        name = unicode('%s %s %s %s' % (title,start,description,end)).encode('utf-8')
        items.append({'type':'video', 'mode':'play_tv', 'name':name, 'id':link, 'description':'', 'duration':'0'})
    items.append({'type':'dir', 'mode':'livestream', 'name':'LIVESTREAM', 'id':'', 'description':'', 'duration':'0'})
    return items

def get_live_video_items(data):
    items = []
    live = re.search('id="stream_tile_livestream"(.*?)<hr>', data, re.S)
    if live:
        a = live.group(1)
        items = get_event_items(items,a,live=True)
    ondemand = re.search('id="stream_tile_ondemandstream"(.*?)<hr>', data, re.S)
    if ondemand:
        a = ondemand.group(1)
        items = get_event_items(items,a,live=False)
    return items
    
def get_event_items(items,a,live):
    base_url = 'http://tv.sport1.de'
    b = re.findall('<a (.*?)</a>', a, re.S)
    for c in b:
        d = re.search('href="(.+?)"', c, re.S).group(1)
        e = re.search('src="(.+?)"', c, re.S).group(1)
        f = re.search('<span class="Info">(.+?)<br>', c, re.S).group(1)
        g = re.search('<strong>(.+?)</strong>', c, re.S).group(1)
        if not d.startswith('http'):
            d = base_url+d
        if not e.startswith('http'):
            e = base_url+e
        if live:
            h = unicode('%s %s' % (f,g)).encode('latin-1')
        else:
            h = unicode('ARCHIV: %s %s' % (f,g)).encode('latin-1')
        items.append({'type':'video', 'mode':'play_tv', 'name':h, 'id':d, 'image':e, 'description':'', 'duration':'0'})
    return items
    
def get_live_radio_items(data):
    items = []
    for l in data:
        try:
            m = l['season'][0]['round'][0]['match']
            for i in m:
                name = None
                finished = i['finished']
                home = i['home']['name']
                away = i['away']['name']
                match_time = i['match_time']
                match_meta = i.get('match_meta', [])
                current_minute = i.get('current_minute', '')
                result = '%s:%s' % (i['match_result'][0]['match_result'],i['match_result'][1]['match_result'])
                for meta in match_meta:
                    kind = meta['kind']
                    if not 'Konferenz' in str(items) and 'conference' in kind and kind.endswith('.mp3'):
                        id = meta['content']
                        name = '%s: Konferenz' % (match_time)
                        item = {'type':'video', 'mode':'play_video', 'name':name, 'id':id, 'description':'', 'duration':'0'}
                        items.insert(0, item)
                    elif kind.endswith('.mp3'):
                        id = meta['content']
                        name = unicode('%s %s - %s %s %s\'' % (match_time,home,away,result,current_minute)).encode('utf-8')
                if name:
                    item = {'type':'video', 'mode':'play_video', 'name':name, 'id':id, 'description':'', 'duration':'0'}
                    items.append(item)
        except:
            pass
    return items

def get_hls(data,q):
    result = None
    y = ['1500','3000','6000']
    z = y[q]
    pattern2 = '<div class="player".*?src="(.*?)"'
    pattern1 = 'file\s*:\s*"(.*?)"'
    a = re.search(pattern1, data)
    if a:
        s = a
    else:
        s = re.search(pattern2, data)
    if s:
        m3u8 = s.group(1)
        m3u8 = re.sub('b=\d+-\d+', 'b=0-%s' % z, m3u8)
        if not 'b=0' in m3u8:
            m3u8 = '%s&b=0-%s' % (m3u8,z)
        return m3u8
    else:
        pattern = '<div class="player">(?:<p class="error">|<p>)(.*?)</p>'
        s = re.search(pattern, data, re.S)
        if s:
            msg = s.group(1).strip()
            msg = re.sub('(<.+?>)', '', msg)
            return msg
        pattern = '<p class="text">(.+?)</p>'
        s = re.search(pattern, data, re.S)
        if s:
            msg = s.group(1).strip()
            msg = re.sub('(<.+?>)', '', msg)
            return msg
    return result