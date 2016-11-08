#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmcaddon,xbmcplugin,xbmcgui,urllib,sys,re,os

addon = xbmcaddon.Addon()
pluginhandle = int(sys.argv[1])
addonID = addon.getAddonInfo('id')
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.7tv')):
		showPro7 = addon.getSetting("Pro7NI") == "false"
	else:
		showPro7 = False
else:
	showPro7 = addon.getSetting("Pro7") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.7tv')):
		showSat1 = addon.getSetting("Sat1NI") == "false"
	else:
		showSat1 = False
else:
	showSat1=addon.getSetting("Sat1") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.7tv')):
		showKabel1 = addon.getSetting("Kabel1NI") == "false"
	else:
		showKabel1 = False
else:
	showKabel1=addon.getSetting("Kabel1") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.7tv')):
		showSIXX = addon.getSetting("SIXXNI") == "false"
	else:
		showSIXX = False
else:
	showSIXX=addon.getSetting("SIXX") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.7tv')):
		showSat1Gold = addon.getSetting("Sat1GoldNI") == "false"
	else:
		showSat1Gold = False
else:
	showSat1Gold=addon.getSetting("Sat1Gold") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.7tv')):
		showProSiebenMAXX = addon.getSetting("ProSiebenMAXXNI") == "false"
	else:
		showProSiebenMAXX = False
else:
	showProSiebenMAXX=addon.getSetting("ProSiebenMAXX") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.zdf_de_lite')):
		showZDFNeo = addon.getSetting("ZDFNeoNI") == "false"
	else:
		showZDFNeo = False
else:
	showZDFNeo=addon.getSetting("ZDFNeo") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.zdf_de_lite')):
		showZDFKultur = addon.getSetting("ZDFKulturNI") == "false"
	else:
		showZDFKultur = False
else:
	showZDFKultur=addon.getSetting("ZDFKultur") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.zdf_de_lite')):
		showZDFInfo = addon.getSetting("ZDFInfoNI") == "false"
	else:
		showZDFInfo = False
else:
	showZDFInfo=addon.getSetting("ZDFInfo") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.arte_tv')):
		showArte = addon.getSetting("ArteNI") == "false"
	else:
		showArte = False
else:
	showArte=addon.getSetting("Arte") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.kikaninchen')):
		showKikaninchen = addon.getSetting("KikaninchenNI") == "false"
	else:
		showKikaninchen = False
else:
	showKikaninchen=addon.getSetting("Kikaninchen") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.nick_de')):
		showNickelodeon = addon.getSetting("NickelodeonNI") == "false"
	else:
		showNickelodeon = False
else:
	showNickelodeon=addon.getSetting("Nickelodeon") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.nick_de')):
		showNickJr = addon.getSetting("NickJrNI") == "false"
	else:
		showNickJr = False
else:
	showNickJr=addon.getSetting("NickJr") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.nick_de')):
		showNickNight = addon.getSetting("NickNightNI") == "false"
	else:
		showNickNight = False
else:
	showNickNight=addon.getSetting("NickNight") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.orftvthek4de')):
		showORF = addon.getSetting("ORFNI") == "false"
	else:
		showORF = False
else:
	showORF=addon.getSetting("ORF") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.tlc_de')):
		showTLC = addon.getSetting("TLCNI") == "false"
	else:
		showTLC = False
else:
	showTLC=addon.getSetting("TLC") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.mtv_de')):
		showMTV = addon.getSetting("MTVNI") == "false"
	else:
		showMTV = False
else:
	showMTV=addon.getSetting("MTV") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.zdf_de_lite')):
		showZDF = addon.getSetting("ZDFNI") == "false"
	else:
		showZDF = False
else:
	showZDF=addon.getSetting("ZDF") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.ardmediathek_de')):
		showARD = addon.getSetting("ARDNI") == "false"
	else:
		showARD = False
else:
	showARD=addon.getSetting("ARD") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.dmax_de')):
		showDMAX = addon.getSetting("DMAXNI") == "false"
	else:
		showDMAX = False
else:
	showDMAX=addon.getSetting("DMAX") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.kika_de')):
		showKIKA = addon.getSetting("KIKANI") == "false"
	else:
		showKIKA = False
else:
	showKIKA=addon.getSetting("KIKA") == "false"
if addon.getSetting("NichtInstalliert") == "true":
	if os.path.isdir(xbmc.translatePath('special://home/addons/plugin.video.tele5_de')):
		showTELE5 = addon.getSetting("TELE5NI") == "false"
	else:
		showTELE5 = False
else:
	showTELE5=addon.getSetting("TELE5") == "false"
iconPath = 'resources/Media/'
iconPro7=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'pro7.png')
iconSat1=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'sat1.png')
iconKabel1=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'kabel1.png')
iconSIXX=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'sixx.png')
iconSat1Gold=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'sat1gold.png')
iconProSiebenMAXX=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'prosiebenmaxx.png')
iconZDFNeo=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'zdfneo.png')
iconZDFKultur=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'zdfkultur.png')
iconZDFInfo=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'zdfinfo.png')
iconArte=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'arte.png')
iconKikaninchen=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'kikaninchen.png')
iconNickelodeon=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'nickelodeon.png')
iconNickJr=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'nickjr.png')
iconNickNight=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'nicknight.png')
iconORF=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'orf.png')
iconTLC=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'TLC.png')
iconMTV=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'mtv.png')
iconZDF=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'zdf.png')
iconARD=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'ard.png')
iconDMAX=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'dmax.png')
iconKIKA=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'kika.png')
iconTELE5=xbmc.translatePath('special://home/addons/'+addonID+'/'+iconPath+'tele5.png')
fanartNO=xbmc.translatePath('')

def index():
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    if showPro7:
		addDir(translation(30010),"plugin://plugin.video.7tv/pro7/library/",iconPro7,fanartNO)
    if showSat1:
		addDir(translation(30011),"plugin://plugin.video.7tv/sat1/library/",iconSat1,fanartNO)
    if showKabel1:
		addDir(translation(30012),"plugin://plugin.video.7tv/kabel1/library/",iconKabel1,fanartNO)
    if showSIXX:
		addDir(translation(30013),"plugin://plugin.video.7tv/sixx/library/",iconSIXX,fanartNO)
    if showSat1Gold:
		addDir(translation(30014),"plugin://plugin.video.7tv/sat1gold/library/",iconSat1Gold,fanartNO)
    if showProSiebenMAXX:
		addDir(translation(30015),"plugin://plugin.video.7tv/prosiebenmaxx/library/",iconProSiebenMAXX,fanartNO)
    if showZDFNeo:
		addDir(translation(30016),"plugin://plugin.video.zdf_de_lite/?mode=listShows&url=http%3a%2f%2fwww.zdf.de%2fZDFmediathek%2fsenderstartseite%2fsst1%2f1209122",iconZDFNeo,fanartNO)
    if showZDFKultur:
		addDir(translation(30017),"plugin://plugin.video.zdf_de_lite/?mode=listShows&url=http%3a%2f%2fwww.zdf.de%2fZDFmediathek%2fsenderstartseite%2fsst1%2f1317640",iconZDFKultur,fanartNO)
    if showZDFInfo:
		addDir(translation(30018),"plugin://plugin.video.zdf_de_lite/?mode=listShows&url=http%3a%2f%2fwww.zdf.de%2fZDFmediathek%2fsenderstartseite%2fsst1%2f1209120",iconZDFInfo,fanartNO)
    if showArte:
		addDir(translation(30019),"plugin://plugin.video.arte_tv/?mode=list-clusters",iconArte,fanartNO)
    if showKikaninchen:
		addDir(translation(30020),"plugin://plugin.video.kikaninchen/",iconKikaninchen,fanartNO)
    if showMTV:
		addDir(translation(30021),"plugin://plugin.video.mtv_de/?mode=listShows&url=http%3a%2f%2fwww.mtv.de%2fshows%2fasync_data.json%3fsort%3dplayable",iconMTV,fanartNO)
    if showNickelodeon:
		addDir(translation(30022),"plugin://plugin.video.nick_de/?mode=listShows&url=http%3a%2f%2fwww.nick.de%2fvideos",iconNickelodeon,fanartNO)
    if showNickJr:
		addDir(translation(30023),"plugin://plugin.video.nick_de/?mode=listShowsJR&url=http%3a%2f%2fwww.nickjr.de%2fvideos",iconNickJr,fanartNO)
    if showNickNight:
		addDir(translation(30024),"plugin://plugin.video.nick_de/?mode=listShowsNight&url=http%3a%2f%2fwww.nicknight.de",iconNickNight,fanartNO)
    if showORF:
		addDir(translation(30025),"plugin://plugin.video.orftvthek4de/?backdrop=C%3a%5cUsers%5cSteffen%5cAppData%5cRoaming%5cKodi%5caddons%5cplugin.video.orftvthek4de%5cresources%5cmedia%5cfanart_top.png&banner=C%3a%5cUsers%5cSteffen%5cAppData%5cRoaming%5cKodi%5caddons%5cplugin.video.orftvthek4de%5cresources%5cmedia%5cshows_banner.jpg&link&mode=getSendungen&title=Sendungen",iconORF,fanartNO)
    if showTLC:
		addDir(translation(30026),"plugin://plugin.video.tlc_de/?action=showLibrary",iconTLC,fanartNO)
    if showZDF:
		addDir(translation(30027),"plugin://plugin.video.zdf_de_lite/','74','?mode=listAZ&url",iconZDF,fanartNO)
    if showARD:
		addDir(translation(30028),"plugin://plugin.video.ardmediathek_de/','65','?mode=listShowsAZMain&url",iconARD,fanartNO)
    if showDMAX:
		addDir(translation(30029),"plugin://plugin.video.dmax_de/','68','?mode=listAZ&thumb=C%3a%5cUsers%5cSteffen%5cAppData%5cRoaming%5cKodi%5caddons%5cplugin.video.dmax_de%5cicon.png&title&url",iconDMAX,fanartNO)
    if showKIKA:
		addDir(translation(30030),"plugin://plugin.video.kika_de/','71','?audioUrl&mode=listShowsAZ&url",iconKIKA,fanartNO)
    if showTELE5:
		addDir(translation(30031),"plugin://plugin.video.tele5_de/','71','?audioUrl&mode=listShowsAZ&url",iconTELE5,fanartNO)
    xbmcplugin.endOfDirectory(pluginhandle)


def addDir(name,url,iconimage,fanartimage):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image',fanartimage)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)
    return ok


def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

index()
