# -*- coding: utf-8 -*-

from resources.lib.client import Client
from resources.lib import items
from resources.lib import helper
from resources.lib import cache
from resources.lib.common import *

client = Client()

def run():
    if mode == 'root':
        items.channel(client.products())
    elif mode == 'sports':
        data = client.catchups()
        cache.cache_data(data)
        items.sport(data)
    elif mode == 'videos':
        items.video(cache.get_cache_data(),id)
    elif mode == 'play':
        items.play(path())
        
def path():
    master, token = master_token()
    if master and token:
        return index(master, token)
    else:
        return id
        
def master_token():
    if not 'hdnea' in id and '.m3u8' in id:
        token = helper.token(client.token())
        return helper.add_param(id, token), token
    elif 'hdnea' in id and 'm3u8' in id:
        spl = id.split('?')
        if len(spl) == 2:
            return id, spl[1]
    else:
        return None, None

def index(master, token):
    index = helper.index(client.get_data(master))
    if index:
        return helper.add_param(index, token)
    return master

args   = urlparse.parse_qs(sys.argv[2][1:])
mode   = args.get('mode', ['root'])[0]
id     = args.get('id', [''])[0]
params = args.get('params', [''])[0]
log('[eurosportplayer] arguments: %s' % (str(args)))

if mode == 'root':
    if email and password:
        run()
    else:
        addon.openSettings()
else:
    run()