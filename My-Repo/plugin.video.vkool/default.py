import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import urlresolver
import base64
import xbmc
try: import simplejson as json
except ImportError: import json
import cgi
import datetime
from metahandler import metahandlers
from universal import playbackengine, watchhistory

ADDON = xbmcaddon.Addon(id='plugin.video.vkool')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
grab=metahandlers.MetaData()
wh = watchhistory.WatchHistory('plugin.video.vkool')

PATH = "vkool"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-44104701-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.4" #<---- PLUGIN VERSION
homeLink="http://m.vkool.net/"

def __init__(self):
    #print 'this call first'
    self.playlist=sys.modules["__main__"].playlist
    #dialog = xbmcgui.Dialog()
    #if not dialog.yesno(ADDON.getLocalizedString(30000),ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30002), ADDON.getLocalizedString(30003), ADDON.getLocalizedString(30004), ADDON.getLocalizedString(30005)):
    #    return

def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if ADDON.getSetting('auto-view') == 'true':
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting('movies-view') )
                        else:
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting('default-view') )
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting('default-view') )

def GRABMETA(name,year):
        meta = grab.get_meta('movie',name,year,None,None,overlay=6)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels

def HOME():
    
    addDir('[COLOR red][B]SEARCH[/B][/COLOR]','http://m.vkool.net',4,'','','dir')
    
    link = GetContentMob(homeLink)
    try:
        link=link.encode("UTF-8")
    except: pass
   
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('    ','')
    #print link
    matchtop = re.compile('<ul class="navigator"><li><a class="icon-home" href="http://m.vkool.net/">Trang Chủ</a></li>(.+?)</ul>').findall(link)
    #print out the first part of menu
    for vmenu in matchtop:
        submatch=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(vmenu)
        for vsubmenu in submatch:
            vLink, vLinkName=vsubmenu
            addDir('[COLOR blue]-- '+ RemoveHTML(vLinkName).strip()+'[/COLOR]',vLink,2,'','','dir')
    #second part of menu        
    match = re.compile('<div class="glist">(.+?)</div>').findall(link)
    for vmenu in match:
        mainname=re.compile('<h3 class="stitle">(.+?)</h3>').findall(vmenu)[0]
        addDir('[COLOR red][B]***'+mainname+'***[/B][/COLOR]','',2,'','','dir')
        submatch=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(vmenu)
        for vsubmenu in submatch:
            vLink, vLinkName=vsubmenu
            addDir('[COLOR blue]-- '+ RemoveHTML(vLinkName).strip()+'[/COLOR]',vLink,2,'','','dir')

    AUTO_VIEW('')
                   
def INDEX(url):

    BodyIndex(url)
    BodyFooter(url)
    AUTO_VIEW('movies')
                   
def BodyIndex(url):
    try:
        #print url
        link = GetContentMob(url)
        #print 'link ' + link
        try:
            link=link.encode("UTF-8")
        except: pass
        link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('    ','').replace('\'','"').replace('</a><a','</a> <a')
        #print 'link1: ' + link
        matchDiv = re.compile('<div class="content">(.+?)</div>').findall(link)
        #print matchDiv
        match=re.compile('<a href="(.+?)" class="content-items" style="padding:5px!important"><img src="(.+?)" alt="(.+?)" class="album-img" width="120" height="170"><h3>(.+?)</h3><h4>(.+?)</h4><ul class="info-des"><li>Status: <b>(.+?)</b></li><li>Năm: (.+?)</li><li>Thể loại: (.+?) </li>').findall(matchDiv[0])
        #print match
        if(len(match)==0):
            print '------------no match------------ '
        else:
            print 'match in match match'
            
            for vcontent in match:
                (vurl, vimage, valt, vvietname, venglishname, vtype, vyear, vcategory) = vcontent
                data = GRABMETA(venglishname,vyear)
                favtype = 'movie'
                #infoLabels={"Title": venglishname, "year": vyear}
                addDir(vvietname+'-'+venglishname+'('+vyear+')'+' [COLOR yellow]Status: '+vtype+'[/COLOR][COLOR red] Genre: '+vcategory+'[/COLOR]',vurl,7,vimage,data,favtype)
                #print vurl
    except: pass
    
def BodyFooter(url):
    try:
        link = GetContentMob(url)
        #print 'link ' + link
        try:
            link=link.encode("UTF-8")
        except: pass
        link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('    ','').replace('\'','"').replace('</a><a','</a> <a')
        
        pagenum=re.compile('<div class="pagination">(.+?)</div>').findall(link)
        match=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(pagenum[0])
        #pagenum1 = len(pagenum)
        #print match
        for vtemp in match:
            (vurl1, vnum) = vtemp
            vurl = vurl1.replace(' onClick=','')
            addDir(vnum,vurl,2,'','','')
    except: pass
    
def RemoveHTML(inputstring):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', inputstring)
	
def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://m.vkool.net/search/'+searchText+'.html'
        if(searchText == ''):
            HOME()
        else:
            BodyIndex(url)
    except: pass

def Mirrors(url,name):
        #url = 'http://m.vkool.net/info/thuc-tap-sinh-7747.html'
        link = GetContentMob(url)
        #print 'url in mirrors' + url
        link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')       
        try:
            link =link.encode("UTF-8")
        except: pass
        #newlink = ''.join(link.splitlines()).replace('\t','')
        watchOnline=re.compile('<div style="margin-top:10px"><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
        if(watchOnline[0].find("m.vkool.net") > 0):
            #print 'i get here'
            link = GetContentMob(watchOnline[0])
            #print watchOnline[0]
            #print 'link in mirror' + link
            match=re.compile('<div class="server_item"><strong>(.+?)</strong>').findall(link)
            #print match
            for vname in match:
                addDir(vname,watchOnline[0],5,'','','dir')
               # print 'vcontent: ' + vname + ' ' + vurl
        else:
            d = xbmcgui.Dialog()
            d.ok('Coming Soon','Selected Movie is not available','Please choose different movie!!!')
            #xbmc.executebuiltin("XBMC.Notification(Coming Soon!, Please choose different movie!,2000)")
            return
        AUTO_VIEW('')
    #except: pass


def Episodes(url,name):
    #try:
        #print url
        #url = homeLink+'play.php?id=347475'
    link = GetContentMob(url)
    #print 'link in epi ' + url+ link
    match=re.compile('<div class="server_item"><strong>'+name+'</strong><div class="episode_list">(.+?)</div>').findall(link)
    #print match
    mirrors=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match[0])
    #print 'serser: '+ link
    #print mirrors
    
    if(name=="Server Vkool:"):
        addDir("DVD RIP",url,10,'','','dir')
        if(len(mirrors) >= 1):
            match = ''
            (vLink, vLinkName)=mirrors[0]
            link = GetContentMob(vLink)
            match=re.compile('<source src="(.+?)" type="video/mp4" data-quality="hd">').findall(link)
            if 'vkool.net' not in match[0]:
                addDir("HD 720P",url,10,'','','dir')
    else:
        if(len(mirrors) >= 1):
            for mcontent in mirrors:
                vLink, vLinkName=mcontent
                addLink("part -  "+ RemoveHTML(vLinkName).strip(),vLink,3,'','')
            #print 'vlink' + vLink+vLinkName
    #except: pass
            
def EpisodesVkool(url,name):
    #try:
        #print url
    link = GetContentMob(url)
    #print 'link in epi ' + url+ link
    match=re.compile('<div class="server_item"><strong>Server Vkool:</strong><div class="episode_list">(.+?)</div>').findall(link)
    #print match
    mirrors=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match[0])
    #print 'serser: '+ link
    #print mirrors
    
    if(len(mirrors) >= 1):
        match = ''
        for mcontent in mirrors:
            vLink, vLinkName=mcontent
            link = GetContentMob(vLink)
            #link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
            if(name=="DVD RIP"):
                match=re.compile('<source src="(.+?)" type="video/mp4">').findall(link)             
            else:
                match=re.compile('<source src="(.+?)" type="video/mp4" data-quality="hd">').findall(link)
            addLink("part -  "+ RemoveHTML(vLinkName).strip(),match[0].replace(' ', '%20'),3,'','')    
            #addLink("part -  "+ RemoveHTML(vLinkName).strip(),vLink+'++'+vLinkName,3,'',"")
            #print match[0]

def GetDirVideoUrl(url,referr):
    #print 'url in getdirvideourl: ' + url
    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):

        def http_error_302(self, req, fp, code, msg, headers):
            self.video_url = headers['Location']
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302

    redirhndler = MyHTTPRedirectHandler()

    opener = urllib2.build_opener(redirhndler)
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer',referr),
        #('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache'),
        ('Host','www.phimmobile.com')]
    # urllib2.install_opener(opener)
    usock = opener.open(url)
    return redirhndler.video_url
	
 
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except: pass
      # d = xbmcgui.Dialog()
      # d.ok(url,"Can't Connect to site",'Try again in a moment')
	   
def GetContentMob(url):
    opener = urllib2.build_opener()
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer',"http://m.vkool.net/index.php"),
        #('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache'),
        ('Host','m.vkool.net')]
    usock = opener.open(url)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response
	   
def playVideo(videoType,videoId):
    url = ""
    
    if (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def loadVideos(url,name):
        #try:
           print 'url in loadVideos: ' + url
           GA("LoadVideo",name)
           #urlLink = url.split("++")
           #print urlLink
           #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
           xbmc.executebuiltin("XBMC.Notification(Xin Vui lòng chờ!, Đang tải phim,2000)")
           newlink = ''
           if(url.find("redirector.googlevideo.com") > 0 or url.find("ad.dailysach.net") > 0 or url.find("117.103.204.132") > 0):
               playVideo('direct',url)
           else:
               link = GetContentMob(url)
               #print 'link in loadvideo' + url + name + link 
           
               match=re.compile('<script src=\'(.+?)\'></script><div id=\'ooyalaplayer\' style=\'width:640px;height:264px;max-width:100%\'></div>').findall(link)
               if(len(match) == 0):
                   match=re.compile('<iframe width="640" height="270" style="max-width:100%;" src="(.+?)" frameborder="0" allowfullscreen></iframe>').findall(link)
                   if(len(match) == 0):
                       match=re.compile('<iframe width="640" height="389" style="max-width:100%;" src="(.+?)" frameborder="0" allowfullscreen></iframe>').findall(link)              
                       if(len(match) == 0):
                           match=re.compile('<source src="(.+?)" type="video/mp4">').findall(link)
               newlink = match[0]
               print newlink
           #newlink = 'http://ad.dailysach.net/mb/mp4/vkool999epeIp2ivi71kvaWVaKeiimyOqtRivLnhqMOAfmiRf3ZwkHmPZpB7p2iMgnttj3GnlJKzuW3In-Jkm7qJhM6To27Dm5egzL_lmcK_h6m7xKOgyK7KnM-O7GqQh3hqi392dJB6i2ePfqFjj4d4ZQ==/video/ZGZ4ZGp2ZQH4ZN==-480.mp4'
               if(newlink == '' or newlink.find("player.ooyala.com") > 0):
                   d = xbmcgui.Dialog()
                   d.ok('Not Implemented','No playable streams found','Please choose different server!!!')
               elif(newlink.find("zing") > 0):
                   playVideo("direct",newlink)
               else:
                   sources = []
                   label=name
                   hosted_media = ""
                   if(newlink.find("youtube") > 0):
                       lastmatch=""
                       match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
                       #IF MATCH
                       if(len(match) > 0):
                           lastmatch = match[0][len(match[0])-1].replace('v/','')
                       #IF ID FOUND
                       if(len(lastmatch) > 0):
                           print lastmatch
                           hosted_media = urlresolver.HostedMediaFile(url='http://youtube.com/watch?v='+lastmatch, title='youtube')
                       else:
                           d = xbmcgui.Dialog()
                           d.ok('Not Implemented','No playable streams found','Please choose different server!!!')
                           return
                   else:        
                       hosted_media = urlresolver.HostedMediaFile(url=newlink, title=label)
                   sources.append(hosted_media)
                   source = urlresolver.choose_source(sources)
                   #print "urlrsolving" + newlink
                   if source:
                       vidlink = source.resolve()
                   else:
                       vidlink =""
                   playVideo("direct",vidlink)
        #except: pass
		

def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(ADDON.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('ga_visitor')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'  =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = ADDON.getSetting('ga_visitor')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
checkGA()

def addLink(name,url,mode,iconimage,mirrorname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirrorname="+urllib.quote_plus(mirrorname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage,labels,favtype):
        contextMenuItems = []
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=labels )
        
        if favtype == 'movie':
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))

                if os.path.exists(xbmc.translatePath("special://home/addons/plugin.video.collective")):
                        contextMenuItems.append(('Search The Collective', 'XBMC.Container.Update(%s?mode=51&url=url&name=%s)' % ('plugin://plugin.video.collective/', name)))

        liz.addContextMenuItems(contextMenuItems, replaceItems=False)

        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return ok


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param



params=get_params()
url=None
name=None
mode=None
formvar=None
mirrorname=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        mirrorname=urllib.unquote_plus(params["mirrorname"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
        GA("HOME","home")
        HOME()
elif mode==2:
        GA("INDEX",name)
        INDEX(url)
elif mode==3:
        loadVideos(url,mirrorname)
elif mode==4:
        SEARCH()
elif mode==5:
       GA("Episodes",name)
       Episodes(url,name)
elif mode==6:
       SearchResults(url)
elif mode==7:
       Mirrors(url,name)
elif mode==8:
        MirrorsThe(name,url)
elif mode==9:
       INDEX(url)
elif mode==10:
       EpisodesVkool(url,name)


xbmcplugin.endOfDirectory(int(sysarg))
