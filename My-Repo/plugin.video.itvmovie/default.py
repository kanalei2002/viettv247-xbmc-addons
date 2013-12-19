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

ADDON = xbmcaddon.Addon(id='plugin.video.itvmovie')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))

PATH = "itvmovie"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-44104701-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.2" #<---- PLUGIN VERSION
homeLink="http://itvmovie.eu"
mobileurl="http://itvmovie.eu/m"

def __init__(self):
    self.playlist=sys.modules["__main__"].playlist

def HOME():
    
    addDir('SEARCH','http://itvmovie.eu',4,'')
    addDir('*** MOVIES ***','',2,'')
    addDir('+ Action Movies','http://itvmovie.eu/action-movie/',2,'')
    addDir('+ Adventure Movies','http://itvmovie.eu/adventure-movie/',2,'')
    addDir('+ Animation - Cartoon Movies','http://itvmovie.eu/animation-cartoon-movie/',2,'')
    addDir('+ Comedy Movies','http://itvmovie.eu/comedy-movie/',2,'')
    addDir('+ Romance Movies','http://itvmovie.eu/romance-movie/',2,'')
    addDir('+ Crime - Mystery Movies - US','http://itvmovie.eu/crime-mystery-movie/',2,'')
    addDir('+ Horror Movies','http://itvmovie.eu/horror-movie/',2,'')
    addDir('+ Science Fiction Movies','http://itvmovie.eu/science-fiction-movie/',2,'')
    addDir('+ History - Kungfu Movies','http://itvmovie.eu/history-kungfu-movie/',2,'')
    addDir('+ Family Movies','http://itvmovie.eu/family-movie/',2,'')
    addDir('+ Documentary Movies','http://itvmovie.eu/documentary-movie/',2,'')
    addDir('+ Music Movies','http://itvmovie.eu/music-movie/',2,'')
    addDir('+ Sports Movies','http://itvmovie.eu/sports-movie/',2,'')
    addDir('+ War Movies','http://itvmovie.eu/war-movie/',2,'')
    addDir('+ Western Movies','http://itvmovie.eu/western-movie/',2,'')
    addDir('*** TV SHOWS ***','',2,'')
    addDir('+ Drama TV','http://itvmovie.eu/drama-tv-shows/',2,'')
    addDir('+ Action - Adventure TV','http://itvmovie.eu/action-adventure-tv-shows/',2,'')
    addDir('+ Animation TV','http://itvmovie.eu/animation-tv-shows/',2,'')
    addDir('+ Romance TV','http://itvmovie.eu/romance-tv-shows/',2,'') 
    addDir('+ Comedy TV','http://itvmovie.eu/comedy-tv-shows/',2,'')
    addDir('+ Crime - Mystery TV','http://itvmovie.eu/crime-mystery-tv-shows/',2,'')
    addDir('+ Family TV','http://itvmovie.eu/family-tv-shows/',2,'')
    addDir('+ Science - Fiction TV','http://itvmovie.eu/science-fiction-tv-shows/',2,'')
    addDir('+ History TV','http://itvmovie.eu/history-tv-shows/',2,'')
    addDir('+ Hot TV','http://itvmovie.eu/hot-tv-show/',2,'')
    addDir('+ Documentary TV','http://itvmovie.eu/documentary-tv-shows/',2,'')
        
def INDEX(url):
    
    try:
        link = GetContent(url)
        link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('    ','').replace('<div class="BlockProduct2 hot-movie"> <span class="icon-hot"></span>','<div class="BlockProduct2 "> ').replace('<span class="icon-hot"></span>','')
        print 'link: ' + link
        match=re.compile('<div class="BlockProduct2 ">  <a href="(.+?)" class="img" title="(.+?)"><img src="(.+?)" width="120" height="160" alt=".+?" title=".+?"/></a>   <a href=".+?" class="NameProduct" title=".+?">.+?</a> <span class="hd">(.+?)</span> <span class="tap">(.+?)</span> ').findall(link)
        #print match
        if(len(match)==0):
            print '------------no match------------ '
        else:
            print 'match in match match'
            dialogWait = xbmcgui.DialogProgress()
            ret = dialogWait.create('Please wait until Movie list is loaded.')
            totalLinks = len(match)
            loadedLinks = 0
            remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(0, '[B]Movies list is loading[/B]',remaining_display)
            for vcontent in match:
                (vurl, vname, vimage, vyear, vstatus) = vcontent
                #print vcontent
                if (vimage.find("http://") == -1):
                    vimage = homeLink+vimage
        
                vidid=re.compile('<p style="padding-top:10px"><a href="(.+?)" title="(.+?)">').findall(GetContent(homeLink+vurl))
                if "</span>" in vstatus:
                    addDir('[COLOR orange]'+vname+'[/COLOR]'+' [COLOR red]['+vyear+'][/COLOR]',homeLink+vurl,7,vimage)
                else:
                    addDir('[COLOR orange]'+vname+'[/COLOR]'+' [COLOR red]['+vstatus+'-'+vyear+'][/COLOR]',homeLink+vurl,7,vimage)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Movies list is loading[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
            dialogWait.close()
            del dialogWait
            
        pagetemp=re.compile('<div class="fr_page_links">(.+?)</div>').findall(link)
        pagenum=re.compile('<a href="(.+?)" rel="(.+?)">(.+?)</a>').findall(pagetemp[0])    
        print pagenum
        for vurl, vrel, vnum in pagenum:
            if(vnum != "Live sport"):
                if(vnum == 'Prev'):
                    addDir("[COLOR green]"+vnum+"[/COLOR]",homeLink+vurl,2,"")
                else:
                    addDir("[COLOR red]page: " + vnum+"[/COLOR]",homeLink+vurl,2,"")
        pagenum1=re.compile('<a class="last" href="(.+?)" rel="(.+?)">(.+?)</a>').findall(link)
        for vurl, vrel, vnum in pagenum1:
            addDir("[COLOR green]"+vnum+"[/COLOR]",homeLink+vurl,2,"")
        #print 'pagenum1 ' + vnum
    except: pass


def VIEWS():
        if ADDON.getSetting("auto-view") == "true":
                if ADDON.getSetting("choose-skin") == "true":
                        if ADDON.getSetting("con-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif ADDON.getSetting("con-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(51)")
                        elif ADDON.getSetting("con-view") == "2":
                                xbmc.executebuiltin("Container.SetViewMode(500)")
                        elif ADDON.getSetting("con-view") == "3":
                                xbmc.executebuiltin("Container.SetViewMode(501)")
                        elif ADDON.getSetting("con-view") == "4":
                                xbmc.executebuiltin("Container.SetViewMode(508)")
                        elif ADDON.getSetting("con-view") == "5":
                                xbmc.executebuiltin("Container.SetViewMode(504)")
                        elif ADDON.getSetting("con-view") == "6":
                                xbmc.executebuiltin("Container.SetViewMode(503)")
                        elif ADDON.getSetting("con-view") == "7":
                                xbmc.executebuiltin("Container.SetViewMode(515)")
                        return
                elif ADDON.getSetting("choose-skin") == "false":
                        if ADDON.getSetting("xpr-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif ADDON.getSetting("xpr-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(52)")
                        elif ADDON.getSetting("xpr-view") == "2":
                                xbmc.executebuiltin("Container.SetViewMode(501)")
                        elif ADDON.getSetting("xpr-view") == "3":
                                xbmc.executebuiltin("Container.SetViewMode(55)")
                        elif ADDON.getSetting("xpr-view") == "4":
                                xbmc.executebuiltin("Container.SetViewMode(54)")
                        elif ADDON.getSetting("xpr-view") == "5":
                                xbmc.executebuiltin("Container.SetViewMode(60)")
                        elif ADDON.getSetting("xpr-view") == "6":
                                xbmc.executebuiltin("Container.SetViewMode(53)")
                        return
        else:
                return
        	
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
        url = 'http://itvmovie.eu/search/?tk='+searchText
        if(searchText == ''):
            HOME()
        else:
            INDEX(url)
    except: pass

def Mirrors(url,name):      
        link = GetContent(url)
        #link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        #print url+link
        try:
            link =link.encode("UTF-8")
        except: pass
        #newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<p style="padding-top:10px"><a href="(.+?)" title="(.+?)">').findall(link)
        newlink = match[0]
        reallink = mobileurl+newlink[0].replace('watch-movie-online','watch-online')
        #print reallink
        moblink = GetContentMob(reallink)
        #print moblink
        vnametemp=re.compile('<div class="serverlist"><span>(.+?)</span> <a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(moblink)
        for vcontent in vnametemp:
            vname, vurl=vcontent
            addDir(vname,mobileurl+'/'+vurl,5,"")
           # print 'vcontent: ' + vname + ' ' + vurl


    #except: pass


def Episodes(url,name):
    #try:
        link = GetContentMob(url)
        match=re.compile('<div class="serverlist"><span>'+name+'</span> (.+?)</div>').findall(link)
        mirrors=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match[0])
        if(len(mirrors) >= 1):
            for mcontent in mirrors:
                vLink, vLinkName=mcontent
                addLink("part -  "+ RemoveHTML(vLinkName).strip(),mobileurl+"/"+vLink,3,'',"")
                   # print 'vLink, vLinkName: ' + vLink + ' ' + vLinkName

    #except: pass

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
	   
def playVideo(videoType,videoId):
    url = ""
    #if (videoType == "youtube"):
    #    try:
    #        url = getYoutube(videoId)
    #        xbmcPlayer = xbmc.Player()
    #        xbmcPlayer.play(url)
    #    except:
            #url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
    #        url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoId
    #        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
        #url = 'plugin://plugin.video.youtube/?action=play_video&videoid=SPn106LGnjU'
        #print 'url: ' + url
        #xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(url)
    if (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def loadVideos(url,name):
        #try:
           #print 'url in loadVideos: ' + url
           #url = 'http://phim.xixam.com/xem-online/the-chien-z-15275-1-8.html'
           GA("LoadVideo",name)
           #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
           xbmc.executebuiltin("XBMC.Notification(Please Wait, Resolving Link!,2000)")
           link=GetContentMob(url)
           try:
                   link =link.encode("UTF-8")                   
           except: pass
           newlink = ''.join(link.splitlines()).replace('\t','')
           #print 'newlink: ' + newlink
           match=re.compile('<source [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
           #newlink=GetDirVideoUrl(viddomain+match[0],url)
           #print 'newlink in loadVideos: ' + match[0]
           if (len(match) == 0): 
               match=re.compile('<video [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*></video>').findall(newlink)
           if (len(match) == 0):
               match=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*></iframe>').findall(newlink)
           newlink = match[0]
           #print newlink
           if (newlink.find("dailymotion") > 0):
                match=re.compile('http://www.dailymotion.com/embed/video/(.+?)\?').findall(newlink)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(newlink+"&dk;")
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(newlink)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                #print 'link in loadVideo: ' + link
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('<param name="flashvars" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                print 'in dailymontion:' + str(newseqeunce)
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"video_url":"(.+?)",').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                vidlink=urllib2.unquote(dm_low[0]).decode("utf8")
                playVideo('dailymontion',vidlink)
           elif (newlink.find("video.google.com") > 0):
                match=re.compile('http://video.google.com/videoplay.+?docid=(.+?)&.+?').findall(newlink)
                glink=""
                if(len(match) > 0):
                        glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                else:
                        match=re.compile('http://video.google.com/googleplayer.swf.+?docId=(.+?)&dk').findall(newlink)
                        if(len(match) > 0):
                                glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                gcontent=re.compile('<div class="mod_download"><a href="(.+?)" title="Click to Download">').findall(glink)
                if(len(gcontent) > 0):
                        playVideo('google',gcontent[0])
           elif (newlink.find("docs.google.com") > 0):
               playVideo('direct',newlink)
           elif (newlink.find("redirector.googlevideo.com") > 0):
               playVideo('direct',newlink)
           elif (newlink.find("4shared") > 0):
               d = xbmcgui.Dialog()
               d.ok('Not Implemented','Sorry 4Shared links',' not implemented yet')
           #elif(newlink.find("youtube") > 0):
           #    lastmatch=""
           #    match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
           #    #IF MATCH
           #    if(len(match) > 0):
           #            lastmatch = match[0][len(match[0])-1].replace('v/','')
           #    #IF ID FOUND
           #    if(len(lastmatch) > 0):
           #        sources = []
           #        hosted_media = urlresolver.HostedMediaFile(url='http://youtube.com/watch?v='+lastmatch, title='youtube')
           #        #hosted_media = urlresolver.HostedMediaFile(url='http://flashx.tv/video/2WHYHYMXHKO3/NEW-JAVMONCOM-heyzo0421-A', title='youtube')
           #        sources.append(hosted_media)
           #        source = urlresolver.choose_source(sources)
           #        if source:
           #            stream_url = source.resolve()
           #            playVideo("direct",stream_url)
           #    else:
           #        d = xbmcgui.Dialog()
           #        d.ok('Not Implemented','No playable streams found','Please choose different server!!!')
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
