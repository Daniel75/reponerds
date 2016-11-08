# -*- coding: utf-8 -*-

from common import *

datapath = utfenc(xbmc.translatePath('special://profile/addon_data/'+addon_id+'/'))
file = os.path.join(datapath,'cache.json')

def get_cache_data():
    data = None
    if os.path.isfile(file):
        f = xbmcvfs.File(file, 'r')
        data = json.load(f)
        f.close()
    return data

def cache_data(data):
    try:
        f = xbmcvfs.File(file, 'w')
        json.dump(data, f)
        f.close()
    except:
        pass