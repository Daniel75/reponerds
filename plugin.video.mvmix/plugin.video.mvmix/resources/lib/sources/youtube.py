# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests
from resources.lib import common
import json, urlparse, re, urllib
from .signature.cipher import Cipher

site = 'youtube'
yt_proxy = common.yt_proxy()
if yt_proxy:
    location = common.proxy_location()
    site = 'yt_proxy'

def get_videos(artist):
    videos = []
    trusted_channel = None
    url = 'https://www.googleapis.com/youtube/v3/search'
    headers = {'Host': 'www.googleapis.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.36 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate'}
    params = {'part':'snippet','type':'video','maxResults':'50',#'videoDefinition':'high',
                'q':'%s official' % artist,'key':'AIzaSyCky6iU_p2VjvpXwTSOpPVLsGFIdR51lQE',
                }
    if yt_proxy:
        try:
            json_data = pxy_request(url, params).json()
        except:
            return False
    else:
        try:
            json_data = requests.get(url, params=params, headers=headers).json()
        except:
            return False
    try:
        items = json_data['items']
        first = True
        for item in items:
            try:
                id = item['id']['videoId']
                snippet = item['snippet']
                t = snippet['title'].encode('utf-8')
                try:
                    t = re.sub('「',' - ', t)
                except:
                    pass
                t = t.replace('–', '-')
                spl = t.split(' - ')
                name = spl[0].strip().decode('utf-8')
                title = spl[1].strip().decode('utf-8')
                if len(spl) > 2:
                    title = '%s - %s' % (title, spl[2].strip().decode('utf-8'))
                description = snippet['description'].lower().encode('utf-8')
                channel = snippet['channelTitle'].lower().replace(' ','').encode('utf-8')
                name = check_name(artist,name)
                if artist.lower() == name.encode('utf-8').lower():
                    if status(trusted_channel,channel,artist,title,description) == True:
                        image = snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
                        duration = ''
                        title = clean_title(title)
                        videos.append({'site':site, 'artist':[name], 'title':title, 'duration':duration, 'id':id, 'image':image})
                        if first == True:
                            trusted_channel = channel
            except:
                pass
            first = False
    except:
        pass
    return videos
    
def get_video_url(id):
    video_url = None
    headers = {'Host': 'www.youtube.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.36 Safari/537.36',
                'Referer': 'https://www.youtube.com',}
    params = {'v': id}
    url = 'https://youtube.com/watch'
    html = ''
    cookie = ''
    if yt_proxy:
        try:
            token = common.get_yt_pxy_token()
            r = pxy_request(url, params)
            html = r.text
            c = r.headers.get('set-cookie')
            s = re.search('s=(.+?)(?:$|;)', c)
            if s and token:
                cookie = 's=%s; token=%s' % (s.group(1), token)
        except:
            pass
    else:
        try:
            html = requests.get(url, params=params, headers=headers).text
        except:
            pass
    pos = html.find('<script>var ytplayer')
    if pos >= 0:
        html2 = html[pos:]
        pos = html2.find('</script>')
        if pos:
            html = html2[:pos]
    #proxy html
    else:
        p = re.search('<source src="(.+?)"', html, re.DOTALL)
        if p and cookie:
            src = '%s|Cookie=%s' % (p.group(1),urllib.quote_plus(cookie))
            return src
        else:
            return video_url
    #standard html
    re_match_js = re.search(r'\"js\"[^:]*:[^"]*\"(?P<js>.+?)\"', html)
    js = ''
    cipher = None
    if re_match_js:
        js = re_match_js.group('js').replace('\\', '').strip('//')
        cipher = Cipher(java_script_url=js)
        
    re_match = re.search(r'\"url_encoded_fmt_stream_map\"\s*:\s*\"(?P<url_encoded_fmt_stream_map>[^"]*)\"', html)
    if re_match:
        url_encoded_fmt_stream_map = re_match.group('url_encoded_fmt_stream_map')
        url_encoded_fmt_stream_map = url_encoded_fmt_stream_map.split(',')
        for value in url_encoded_fmt_stream_map:
            value = value.replace('\\u0026', '&')
            attr = dict(urlparse.parse_qsl(value))
            url = attr.get('url', None)
            if url:
                url = urllib.unquote(attr['url'])
                if 'signature' in url:
                    video_url = url
                    break
                signature = ''
                if attr.get('s', ''):
                    signature = cipher.get_signature(attr['s'])
                elif attr.get('sig', ''):
                    signature = attr.get('sig', '')
                if signature:
                    url += '&signature=%s' % signature
                    video_url = url
                    break
    return video_url
    
def status(trusted_channel,channel,artist,title,description):
    title = title.lower()
    artist = artist.lower().replace(' ','')
    a = ['lyric', 'no official', 'not official', 'unofficially', 'vevo']
    if any(x in title for x in a):
        if 'official lyric video' in title:
            return True
        else:
            return False
    b = ['parody', 'parodie', 'fan made', 'fanmade', 'vocal cover',
        'custom video', 'music video cover', 'music video montage', 
        'guitar cover', 'drum through', 'guitar walk', 'drum walk',
        'guitar demo', '(drums)', 'drum cam',
        'drumcam', '(guitar)',
        'our cover of', 'in this episode of', 'official comment',
        'full set', 'full album stream',
        '"reaction"', 'reaction!', 'video reaction',
        'splash news']
    if any(x in title for x in b) or any(x in description for x in b):
        return False
    c = [' animated ']
    if any(x in description for x in c):
        return False
    d = [u"\u2665", u"\u2661", 'cover by']
    if any(x in title for x in d):
        return False
    e = ['official video', 'music video', 'taken from', 'itunes.apple.com', 'smarturl.it', 'j.mp']
    if any(x in description for x in e):
        return True
    f = ['official video', 'music video', 'us version']
    if any(x in title for x in f):
        return True
    g = ['records', 'official']
    if any(x in channel for x in g):
        return True
    h = ['vevo']
    if any(channel.endswith(x) for x in h):
        return True
    if trusted_channel == channel:
        return True

def clean_title(title):
    title = re.sub('"|\'|hd|hq|1080p|720p|60\s*fps', '', title, flags=re.I)
    try: title = title.split('|')[0]
    except: pass
    try: title = title.split(' - ')[0]
    except: pass
    title = title.strip()
    return title
    
def check_name(artist,name):
    if not artist.lower() == name.encode('utf-8').lower():
        split_tags = [',','&','feat','ft']
        for tag in split_tags:
            if tag in name:
                splitted = name.split(tag)
                if len(splitted) > 1:
                    name = splitted[0].strip()
                    break
    return name

def pxy_request(url,params):
    proxfree = 'https://www.proxfree.com'
    headers = headers={'User-Agent':'iPhone'}
    r = requests.head(proxfree, headers=headers, stream=True)
    cookie = r.headers.get('set-cookie')
    s = re.search('s=(.+?)(?:$|;)', cookie)
    token = re.search('token=(.+?)(?:$|;)', cookie)
    if s and token:
        cookie = 's=%s; token=%s; default=5' % (s.group(1),token.group(1))
        common.set_yt_pxy_token(token.group(1))
    proxy = 'https://%s.proxfree.com/request.php?do=go' % location
    headers.update({'Cookie':cookie})
    if params:
        link = '%s?%s' % (url,urllib.urlencode(params))
    else:
        link = url
    form_data = {'get':link, 'pfserverDropdown':proxy, 'pfipDropdown':'default'}
    response = requests.post(proxy, headers=headers, data=form_data)
    return response