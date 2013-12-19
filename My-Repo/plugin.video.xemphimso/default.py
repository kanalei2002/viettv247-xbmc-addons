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

ADDON = xbmcaddon.Addon(id='plugin.video.xemphimso')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "xemphimso"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-44104701-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.0" #<---- PLUGIN VERSION
homeLink="http://m.xemphimso.com/"
mobileurl="http://m.xemphimso.com"

def __init__(self):
    #print 'this call first'
    self.playlist=sys.modules["__main__"].playlist
    #dialog = xbmcgui.Dialog()
    #if not dialog.yesno(ADDON.getLocalizedString(30000),ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30002), ADDON.getLocalizedString(30003), ADDON.getLocalizedString(30004), ADDON.getLocalizedString(30005)):
    #    return

def HOME():
    
    addDir('SEARCH','http://m.xemphimso.com',4,'')
    addDir('[COLOR red][B]*** PHIM BỘ ***[/COLOR][/B]','',2,'')
    addDir('[COLOR green]+ Phim Việt Nam[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-viet-nam_1/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Trung Quốc[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-trung-quoc_2/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Hàn Quốc[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-han-quoc_3/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Đài Loan[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-dai-loan_4/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Mỹ[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-my_5/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Châu Âu[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-chau-au_6/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Nhật Bản[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-nhat-ban_7/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Hồng Kông[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-hong-kong_8/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Thái Lan[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-thai-lan_9/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Châu Á[/COLOR]','http://m.xemphimso.com/quoc-gia-phim-chau-a_12/page-1.html',2,'')
    addDir('[COLOR red][B]*** PHIM LẺ ***[/COLOR][/B]','',2,'')
    addDir('[COLOR green]+ Phim Chiếu Rạp[/COLOR]','http://m.xemphimso.com/the-loai-phim-chieu-rap_24/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Hành Động[/COLOR]','http://m.xemphimso.com/the-loai-phim-hanh-dong_1/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Phiêu Lưu[/COLOR]','http://m.xemphimso.com/the-loai-phim-phieu-luu_2/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Kinh Dị[/COLOR]','http://m.xemphimso.com/the-loai-phim-kinh-di_3/page-1.html',2,'')  
    addDir('[COLOR green]+ Phim Tình Cảm[/COLOR]','http://m.xemphimso.com/the-loai-phim-tinh-cam_4/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Hoạt Hình[/COLOR]','http://m.xemphimso.com/the-loai-phim-hoat-hinh_5/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Võ Thuật[/COLOR]','http://m.xemphimso.com/the-loai-phim-vo-thuat_6/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Hài Hước[/COLOR]','http://m.xemphimso.com/the-loai-phim-hai-huoc_7/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Âm Nhạc[/COLOR]','http://m.xemphimso.com/the-loai-phim-am-nhac_18/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Tâm Lý[/COLOR]','http://m.xemphimso.com/the-loai-phim-tam-ly_8/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Viễn Tưởng[/COLOR]','http://m.xemphimso.com/the-loai-phim-vien-tuong_9/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Thần Thoại[/COLOR]','http://m.xemphimso.com/the-loai-phim-than-thoai_10/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Chiến Tranh[/COLOR]','http://m.xemphimso.com/the-loai-phim-chien-tranh_11/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Hình Sự[/COLOR]','http://m.xemphimso.com/the-loai-phim-hinh-su_14/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Dã Sử[/COLOR]','http://m.xemphimso.com/the-loai-phim-da-su_12/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Thể Thao[/COLOR]','http://m.xemphimso.com/the-loai-phim-the-thao_13/page-1.html',2,'')
    addDir('[COLOR red][B]*** TOP PHIM ***[/COLOR][/B]','',2,'')
    addDir('[COLOR green]+ Phim Lẻ Mới[/COLOR]','http://m.xemphimso.com/danh-sach/phim-le/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Bộ Mới[/COLOR]','http://m.xemphimso.com/danh-sach/phim-bo/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Đánh Giá Cao[/COLOR]','http://m.xemphimso.com/danh-sach/binh-chon-nhieu/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Xem Nhiều[/COLOR]','http://m.xemphimso.com/danh-sach/xem-nhieu/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Chiếu Rạp[/COLOR]','http://m.xemphimso.com/danh-sach/phim-chieu-rap/page-1.html',2,'')
    addDir('[COLOR green]+ Phim Xem Nhiều Trong Ngày[/COLOR]','http://m.xemphimso.com/danh-sach/xem-nhieu-trong-ngay/page-1.html',2,'')
            
def INDEX(url):

    try:
        #url = 'http://m.xemphimso.com/quoc-gia-phim-trung-quoc_2/page-1.html'
        link = GetContentMob(url)
        try:
            link=link.encode("UTF-8")
        except: pass
        link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('    ','')
        #print 'link: ' + link
        match=re.compile('<!-- #BEGIN list_item --><div class="row"><div class="img-80"><a href="(.+?)"><img src="(.+?)" width="80" height="120"></a></div><div class="txt-80"><h3><a href="(.+?)" class="title">(.+?)</a>').findall(link)
        #print match
        if(len(match)==0):
            print '------------no match------------ '
        else:
            #print 'match in match match'
            dialogWait = xbmcgui.DialogProgress()
            ret = dialogWait.create('Please wait until Movie list is loaded.')
            totalLinks = len(match)
            loadedLinks = 0
            remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(0, '[B]Movies list is loading[/B]',remaining_display)
            for vcontent in match:
                (vurl, vimage, vurl1, vname) = vcontent                
                addDir(vname,vurl,7,vimage)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Movies list is loading[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
            dialogWait.close()
            del dialogWait
        #print footer    
        pagenum=re.compile('<OPTION  value="(.+?)">(.+?)</OPTION>').findall(link)
        pagenum1 = len(pagenum)
        #print pagenum1
        for vurl, vnum in pagenum:
            vurl1 = vurl.replace('page-1.html/page','page')
            addDir(vnum,homeLink+vurl1,2,"")
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
        link = GetContentMob(url)
        #link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        print url+link
        try:
            link =link.encode("UTF-8")
        except: pass
        #newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div class="listserver"><span class="name">(.+?)</span>').findall(link)
        
        for vname in match:
            addDir(vname,url,5,"")
           # print 'vcontent: ' + vname + ' ' + vurl


    #except: pass


def Episodes(url,name):
    #try:
        #print url
        #url = homeLink+'play.php?id=347475'
        link = GetContentMob(url)
        match=re.compile('<div class="listserver"><span class="name">'+name+'</span>(.+?)&nbsp; </div>').findall(link)
        mirrors=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match[0])
        #print 'serser: '+ link
        print mirrors
        if(len(mirrors) >= 1):
            for mcontent in mirrors:
                vLink, vLinkName=mcontent
                addLink("tập -  "+ RemoveHTML(vLinkName).strip(),homeLink+vLink,3,'',"")
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
           #print 'url in loadVideos: ' + url
           #url = 'http://phim.xixam.com/xem-online/the-chien-z-15275-1-8.html'
           GA("LoadVideo",name)
           #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
           xbmc.executebuiltin("XBMC.Notification(Xin Vui lòng chờ!, Đang tải phim,2000)")
           link = GetContentMob(url)
        #        #print linktemp
           newlink=''
           match=re.compile('<link rel="canonical" href="(.+?)">').findall(link)
           if(len(match)==0):
               match=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
               for lcontent in match:
                   vurl, vresolution = lcontent
                   if(vresolution=='480p'):
                       newlink = vurl
                   if(vresolution=='720p'):
                       newlink = vurl                   
           else:
               newlink = match[0]
          
           if(newlink == ''):
                d = xbmcgui.Dialog()
                d.ok('Not Implemented','No playable streams found','Please choose different server!!!')
           elif (newlink.find("dailymotion") > 0):
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
           elif(newlink.find("cdn.scity.tv") > 0):
               playVideo('direct',newlink)
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
