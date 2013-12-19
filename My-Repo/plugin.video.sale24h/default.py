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

ADDON = xbmcaddon.Addon(id='plugin.video.sale24h')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "sale24h"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-44104701-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.0" #<---- PLUGIN VERSION
homeLink="http://sale24h.vn/raovat/"
#mobileurl="http://m.xemphimso.com"

def __init__(self):
    #print 'this call first'
    self.playlist=sys.modules["__main__"].playlist
    #dialog = xbmcgui.Dialog()
    #if not dialog.yesno(ADDON.getLocalizedString(30000),ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30002), ADDON.getLocalizedString(30003), ADDON.getLocalizedString(30004), ADDON.getLocalizedString(30005)):
    #    return

def HOME():
    
    INDEX('http://sale24h.vn/raovat/forumdisplay.php?f=112&order=des')
           
def INDEX(url):

    try:
        #print 'url ' + url
        #url = 'http://player.vimeo.com/video/35996642/'
        link = GetContent(url)
        try:
            #link = link.decode("ascii",ignore)
            link=link.encode("UTF-8")
        except: pass
        #print 'link first' + link
        link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('    ','').replace('amp;','')
        print 'link: ' + link
        print'---------------------------------------------------------------------------------------'
        match=re.compile('<ol id="threads" class="threads">(.+?)</ol>').findall(link)
        match1 = re.compile('<!--  status icon block --><a class="threadstatus" rel="vB::AJAX" ><img src="(.+?)" width="120" height="120" border="0"></a><!-- title / author block --><div class="inner"><h3 class="threadtitle"><a class="title" href="(.+?)" id=".+?">(.+?)</a></h3>').findall(match[0])
        
        #print match1
        if(len(match)==0):
            print '------------no match------------ '
        else:
            #print 'match in match match'
            for vcontent in match1:
                (vimage, vurl, vtitle) = vcontent                
                addDir(vtitle,homeLink+vurl,5,vimage)
                print vimage
               
        pagefirst=re.compile('<span class="first_last"><a rel="start" href="(.+?)" title=".+?">.+?</a></span>').findall(link)
        if pagefirst:
            addDir("First Page",homeLink+pagefirst[0],2,"")
            
        pageprev=re.compile('<span class="prev_next"><a rel="prev" href="(.+?)" title=".+?">.+?</a></span>').findall(link)
        if pageprev:
            addDir("Previous",homeLink+pageprev[0],2,"")
            
        pagenext=re.compile('<span class="prev_next"><a rel="next" href="(.+?)" title=".+?">.+?</a></span>').findall(link)   
        if pagenext:
            addDir("Next",homeLink+pagenext[0],2,"")


        pagelast = re.compile('<span class="first_last"><a href="(.+?)" title=".+?">.+?</a></span>').findall(link)
        if pagelast:
            addDir("Last Page",homeLink+pagelast[0],2,"")
        
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
        url = 'http://m.xemphimso.com/?search='+searchText
        if(searchText == ''):
            HOME()
        else:
            INDEX(url)
    except: pass

def Mirrors(url,name):
        #print url
        link = GetContentMob(url)
        #link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        #print url+link
        try:
            link =link.encode("UTF-8")
        except: pass
        #newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<span class="svname">(.+?) </span>').findall(link)
        #print match
        for vname in match:
            addDir(vname,url,5,"")
           # print 'vcontent: ' + vname + ' ' + vurl


    #except: pass


def Episodes(url,name):
    #try:
        #print 'url episode' + url + name
        #url = homeLink+'play.php?id=347475'
        link = GetContent(url)
        try:
            link=link.encode("UTF-8")
        except: pass
        link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('    ','').replace('amp;','')
        #print link
        matchVimeo=re.compile('<object class="restrain" type="application/x-shockwave-flash" allowfullscreen="true" width="640" height="426" data="(.+?)">').findall(link)
        name = name.split('[')
        if matchVimeo:
            addLink(name[0]+':'+' Vimeo Server',matchVimeo[0],3,'',"vimeo")
        matchYoutube = re.compile('<iframe title="YouTube video player" width="640" height="426" src="//(.+?)" frameborder="0" allowfullscreen></iframe>').findall(link)
        if matchYoutube:
            addLink(name[0]+':'+' Youtube Server',matchYoutube[0],3,'',"youtube")
        matchGoogle = re.compile('<a href="https://picasaweb.google.com/(.+?)" target="_blank">').findall(link)
        if matchGoogle:
            addLink(name[0]+':'+' Picasa Server',matchGoogle[0],3,'',"picasa")
    #except: pass

def GetDirVideoUrl(url,referr):
    print 'url in getdirvideourl: ' + url
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
        ('Referer',"http://itvmovie.eu/m/index.php"),
        #('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache'),
        ('Host','itvmovie.eu')]
    usock = opener.open(url)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response

def postContent(url,data,referr):
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache'),
                         ('Host','www.phim.li')]
    usock=opener.open(url,data)
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
    print videoId
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoId
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def loadVideos(url,name):
        #try:
           print 'url in loadVideos: ' + url + name
           GA("LoadVideo",name)
           #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
           xbmc.executebuiltin("XBMC.Notification(Xin Vui lòng chờ!, Đang tải phim,2000)")
           #link = GetContentMob(url)
           #print url+link
           newlink=''
           #match=re.compile('<source src="(.+?)" type="video/mp4">').findall(link)
           #newlink = match[0]

           if(name=="youtube"):
                vidlink=url.split('embed/')
                playVideo("youtube",vidlink[1])
           elif(name=="vimeo"):
                #vidlink=url.split('=')
                #playVideo("vimeo",vidlink[1])
                d = xbmcgui.Dialog()
                d.ok('Not Implemented','No playable streams found')
           else:
                newlink = 'https://picasaweb.google.com/'+url
                
                vidcontent=postContent("http://player.phim.li/picasaphp/plugins_player.php","iagent=Mozilla%2F5%2E0%20%28Windows%20NT%206%2E1%3B%20WOW64%3B%20rv%3A13%2E0%29%20Gecko%2F20100101%20Firefox%2F13%2E0&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true",homeLink)
                vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
                vidlink=vidmatch[0][0]
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

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
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
       Episodes2(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
