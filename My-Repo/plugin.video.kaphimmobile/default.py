# -*- coding: utf-8 -*-
import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import base64
import xbmc
try: import simplejson as json
except ImportError: import json
import cgi
import datetime

ADDON = xbmcaddon.Addon(id='plugin.video.kaphimmobile')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "kaphimmobile"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-44104701-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.2" #<---- PLUGIN VERSION
homeLink="http://www.kenh88.com"
viddomain="http://www.phimmobile.com"

def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
    addDir('[COLOR red][B]:: Search ::[/B][/COLOR]',homeLink,4,'')   
    
    addDir('[COLOR red][B]:: Phim Bộ-Series ::[/B][/COLOR]','http://www.kenh88.com/phim-bo-series-cat-66-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Hồng Kông[/COLOR]','http://www.kenh88.com/phim-hong-kong-cat-72-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Đài Loan[/COLOR]','http://www.kenh88.com/phim-dai-loan-cat-106-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Hàn Quốc[/COLOR]','http://www.kenh88.com/phim-han-quoc-cat-107-page-1.html',2,'')    
    addDir('[COLOR pink]- Phim Hoạt Hình[/COLOR]','http://www.kenh88.com/phim-hoat-hinh-cat-114-page-1.html',2,'')   
    addDir('[COLOR pink]- Phim Đang Chiếu HOT[/COLOR]','http://www.kenh88.com/phim-bo-dang-chieu-cat-143-page-1.html',2,'')    
    addDir('[COLOR pink]- Hồng Kông English Sub[/COLOR]','http://www.kenh88.com/phim-tvb-english-sub-cat-146-page-1.html',2,'')
    
    addDir('[COLOR red][B]:: Việt Nam ::[/B][/COLOR]','http://www.kenh88.com/viet-nam-cat-80-page-1.html',2,'')
    addDir('[COLOR pink]- Hài Kịch Việt Nam[/COLOR]','http://www.kenh88.com/hai-kich-viet-nam-cat-83-page-1.html',2,'')
    addDir('[COLOR pink]- Nhạc Việt Nam[/COLOR]','http://www.kenh88.com/nhac-viet-nam-cat-88-page-1.html',2,'')
    addDir('[COLOR pink]- Cải Lương[/COLOR]','http://www.kenh88.com/cai-luong-cat-89-page-1.html',2,'')
    addDir('[COLOR pink]- Phóng Sự - Thời Sự[/COLOR]','http://www.kenh88.com/phong-su-thoi-su-cat-117-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Việt Nam[/COLOR]','http://www.kenh88.com/phim-viet-nam-cat-141-page-1.html',2,'')

    addDir('[COLOR red][B]:: Phim Lẻ HK-TQ ::[/B][/COLOR]','http://www.kenh88.com/phim-le-hk-tq-cat-121-page-1.html',2,'')
    addDir('[COLOR pink]- Võ Thuật Kiếm Hiệp[/COLOR]','http://www.kenh88.com/vo-thuat-kiem-hiep-cat-122-page-1.html',2,'')
    addDir('[COLOR pink]- Hành Động - XHĐ[/COLOR]','http://www.kenh88.com/hanh-dong-xhd-cat-123-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Tình Cảm[/COLOR]','http://www.kenh88.com/phim-tinh-cam-cat-124-page-1.html',2,'')
    addDir('[COLOR pink]- Hài - Funny[/COLOR]','http://www.kenh88.com/hai-kich-cat-125-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Ma - Kinh Dị[/COLOR]','http://www.kenh88.com/phim-ma-kinh-di-cat-126-page-1.html',2,'')
    
    addDir('[COLOR red][B]:: Phim Lẻ - HQ ::[/B][/COLOR]','http://www.kenh88.com/phim-le-hq-cat-127-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Hành Động - XHĐ[/COLOR]','http://www.kenh88.com/phim-hanh-dong-xhd-cat-128-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Hài[/COLOR]','http://www.kenh88.com/phim-hai-cat-129-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Ma - Kinh Dị[/COLOR]','http://www.kenh88.com/phim-ma-kinh-di-cat-130-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Tình Cảm[/COLOR]','http://www.kenh88.com/phim-tinh-cam-cat-131-page-1.html',2,'')

    addDir('[COLOR red][B]:: New Release ::[/B][/COLOR]','http://www.kenh88.com/phim-bo-dang-chieu-cat-143-page-1.html',2,'')
    addDir('[COLOR pink]- Phim Rất Hay[/COLOR]','http://www.kenh88.com/?action=newest&q=editorchoice',2,'')
    addDir('[COLOR pink]- Phim Mới[/COLOR]','http://www.kenh88.com/?action=newest&q=newest+phim+online',2,'')
    addDir('[COLOR pink]- Phim Xem Nhiều[/COLOR]','http://www.kenh88.com/?action=topview&q=most+view+phim+online',2,'')    
    addDir('[COLOR pink]- Phim Mới Cập Nhật[/COLOR]','http://www.kenh88.com/?action=newest&q=update',2,'')   

def INDEX(url):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        #newlink = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('    ','')
        #print newlink
        match=re.compile('<div id="makers">(.+?)</div>').findall(newlink)
        for vcontent in match:
            vimage=urllib.quote(re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vcontent)[0])
            #print vimage
            if(vimage.find("http://") == -1):
                  vimage=homeLink+vimage
            #print vimage
            vurl=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vcontent)[0]
            vidid=re.compile('/xem-phim-(.+?)/').findall(vurl)[0] 
            vname=re.compile('<strong >(.+?)</strong>').findall(vcontent)[0]
            addDir('[COLOR orange]'+ vname + '[/COLOR]',vidid,7,vimage)
        pagecontent=re.compile('<span class=pagecur>(.+?)</table>').findall(newlink)
        #print pagecontent
        if(len(pagecontent) >0):
             match5=re.compile("<a class='pagelink' href='(.+?)'>(.+?)</a>").findall(pagecontent[0])
             if(len(match5)==0):
                 match5=re.compile("<A class='pagelink' href='(.+?)'>(.+?)</A>").findall(pagecontent[0])
             for vpage in match5:
                    (vurl,vname)=vpage
                    if(vurl.find("/") == -1):
                        vurl = '/' + vurl
                    addDir("[COLOR red]page: " + vname.encode("utf-8")+'[/COLOR]',homeLink+vurl,2,"")
    #except: pass

	
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
        url = 'http://www.kenh88.com/search.php?q='+searchText+'&btnSort=Search'
        INDEX(url)
    except: pass

def Mirrors(vidid,name):
        url=viddomain+"/index.php?action=view&id="+vidid
        link = GetContentMob(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<td style="text-align:justify" class="movieepisode">(.+?)</td>').findall(newlink)
        for vcontent in match:
            vname=re.compile('<strong>(.+?)</strong>').findall(vcontent)[0]
            addDir(vname,url,5,"")


    #except: pass


def Episodes(url,name):
    #try:
        link = GetContentMob(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<td style="text-align:justify" class="movieepisode"><strong>'+name+'</strong>(.+?)</td>').findall(newlink)
        mirrors=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match[0])
        
        if(len(mirrors) >= 1):
            i = 1
            for mcontent in mirrors:
                vLinktemp, vLinkName=mcontent
                vLink = ''
                j = 1
                k = 1
                for mlink in mirrors:
                    vLink1, vLinkName1 = mlink
                    if(j >= i):
                        if(i == len(mirrors) or j == len(mirrors) or k == 12):
                            vLink += viddomain+vLink1+"+++"+vLinkName1
                        else:
                            vLink += viddomain+vLink1+"+++"+vLinkName1+"***"
                        if(k % 12 == 0):
                            break
                        k += 1
                    j += 1
                i += 1        
                #addLink("tập:  " + RemoveHTML(vLinkName).strip(),mobileurl+"/"+vLink,3,'',"")
                addLink("Tập:  " + RemoveHTML(vLinkName).strip(),vLink,3,'',"")
                print vLink

        #if(len(mirrors) >= 1):
        #        for mcontent in mirrors:
        #            vLink, vLinkName=mcontent
        #            print viddomain+vLink
         #           addLink("part - "+ RemoveHTML(vLinkName).strip(),viddomain+vLink,3,'',"")

    #except: pass

def GetDirVideoUrl(url,referr):

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
        ('User-Agent', 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'),
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
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')
	   
def GetContentMob(url):
    opener = urllib2.build_opener()
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer',"http://www.phimmobile.com/index.php"),
        #('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache'),
        ('Host','www.phimmobile.com')]
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
    if (videoType == "youtube"):
        try:
                url = getYoutube(videoId)
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(url)
        except:
                url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
                xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def loadVideos(url,name):
        #try:
        GA("LoadVideo",name)
        numUrl = url.split('***')
        xbmc.executebuiltin("XBMC.Notification(Đang Tải Phim, Xin Vui Lòng Chờ Chút!,2000)")
        pl=xbmc.PlayList(1)
        pl.clear()
        for realUrl in numUrl:
           linkTap = realUrl.split('+++')
           link=GetContentMob(linkTap[0])
           #print link
           try:
                   link =link.encode("UTF-8")
           except: pass
           newlink = ''.join(link.splitlines()).replace('\t','')
           match=re.compile('<!--ads2<br>--><iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*></iframe>').findall(newlink)
           #print match[0]
           newlink=GetDirVideoUrl(viddomain+match[0],linkTap[0])
           
           #print newlink
           
           if (newlink.find("dailymotion") > -1):
                match=re.compile('http://www.dailymotion.com/embed/video/(.+?)\?').findall(newlink)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(newlink+"&dk;")
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(newlink)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('<param name="flashvars" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                #print 'in dailymontion:' + str(newseqeunce)
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"video_url":"(.+?)",').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                vidlink=urllib2.unquote(dm_low[0]).decode("utf8")
                
                listitem = xbmcgui.ListItem("Phần " + RemoveHTML(linkTap[1]).strip(), thumbnailImage='')
                if(len(match) != 0):
                    url = vidlink
                    #print url
                    xbmc.PlayList(1).add(url, listitem)
                #playVideo('dailymontion',vidlink)
           elif (newlink.find("video.google.com") > -1):
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
           elif (newlink.find("4shared") > -1):
                d = xbmcgui.Dialog()
                d.ok('Not Implemented','Sorry 4Shared links',' not implemented yet')
           else:
                if (newlink.find("linksend.net") > -1):
                     d = xbmcgui.Dialog()
                     d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')
                     
                newlink1 = urllib2.unquote(newlink).decode("utf8")+'&dk;'
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                if(len(match) > 0):
                    videoId = match[0][len(match[0])-1].replace('v/','')
                    try:
                        url = getYoutube(videoId)
                        #xbmcPlayer = xbmc.Player()
                        #xbmcPlayer.play(url)
                    except:
                        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
                        #xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
                        #playVideo('youtube',lastmatch)
                    listitem = xbmcgui.ListItem("Phần " + RemoveHTML(linkTap[1]).strip(), thumbnailImage='')
                    #print url
                    xbmc.PlayList(1).add(url, listitem)
                else:
                    playVideo('phimmobile.com',urllib2.unquote(newlink).decode("utf8"))
        xbmc.Player().play(pl)
        #except: pass
		
def extractFlashVars(data):
    for line in data.split("\n"):
            index = line.find("ytplayer.config =")
            if index != -1:
                found = True
                p1 = line.find("=", (index-3))
                p2 = line.rfind(";")
                if p1 <= 0 or p2 <= 0:
                        continue
                data = line[p1 + 1:p2]
                break
    if found:
            data = json.loads(data)
            flashvars = data["args"]
    return flashvars   
		
def selectVideoQuality(links):
        link = links.get
        video_url = ""
        fmt_value = {
                5: "240p h263 flv container",
                18: "360p h264 mp4 container | 270 for rtmpe?",
                22: "720p h264 mp4 container",
                26: "???",
                33: "???",
                34: "360p h264 flv container",
                35: "480p h264 flv container",
                37: "1080p h264 mp4 container",
                38: "720p vp8 webm container",
                43: "360p h264 flv container",
                44: "480p vp8 webm container",
                45: "720p vp8 webm container",
                46: "520p vp8 webm stereo",
                59: "480 for rtmpe",
                78: "seems to be around 400 for rtmpe",
                82: "360p h264 stereo",
                83: "240p h264 stereo",
                84: "720p h264 stereo",
                85: "520p h264 stereo",
                100: "360p vp8 webm stereo",
                101: "480p vp8 webm stereo",
                102: "720p vp8 webm stereo",
                120: "hd720",
                121: "hd1080"
        }
        hd_quality = 1

        # SD videos are default, but we go for the highest res
        #print video_url
        if (link(35)):
            video_url = link(35)
        elif (link(59)):
            video_url = link(59)
        elif link(44):
            video_url = link(44)
        elif (link(78)):
            video_url = link(78)
        elif (link(34)):
            video_url = link(34)
        elif (link(43)):
            video_url = link(43)
        elif (link(26)):
            video_url = link(26)
        elif (link(18)):
            video_url = link(18)
        elif (link(33)):
            video_url = link(33)
        elif (link(5)):
            video_url = link(5)

        if hd_quality > 1:  # <-- 720p
            if (link(22)):
                video_url = link(22)
            elif (link(45)):
                video_url = link(45)
            elif link(120):
                video_url = link(120)
        if hd_quality > 2:
            if (link(37)):
                video_url = link(37)
            elif link(121):
                video_url = link(121)

        if link(38) and False:
            video_url = link(38)
        for fmt_key in links.iterkeys():

            if link(int(fmt_key)):
                    text = repr(fmt_key) + " - "
                    if fmt_key in fmt_value:
                        text += fmt_value[fmt_key]
                    else:
                        text += "Unknown"

                    if (link(int(fmt_key)) == video_url):
                        text += "*"
            else:
                    print "- Missing fmt_value: " + repr(fmt_key)

        video_url += " | " + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


        return video_url

def getYoutube(videoid):

                code = videoid
                linkImage = 'http://i.ytimg.com/vi/'+code+'/default.jpg'
                req = urllib2.Request('http://www.youtube.com/watch?v='+code+'&fmt=18')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                
                if len(re.compile('shortlink" href="http://youtu.be/(.+?)"').findall(link)) == 0:
                        if len(re.compile('\'VIDEO_ID\': "(.+?)"').findall(link)) == 0:
                                req = urllib2.Request('http://www.youtube.com/get_video_info?video_id='+code+'&asv=3&el=detailpage&hl=en_US')
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                
                flashvars = extractFlashVars(link)

                links = {}

                for url_desc in flashvars[u"url_encoded_fmt_stream_map"].split(u","):
                        url_desc_map = cgi.parse_qs(url_desc)
                        if not (url_desc_map.has_key(u"url") or url_desc_map.has_key(u"stream")):
                                continue

                        key = int(url_desc_map[u"itag"][0])
                        url = u""
                        if url_desc_map.has_key(u"url"):
                                url = urllib.unquote(url_desc_map[u"url"][0])
                        elif url_desc_map.has_key(u"stream"):
                                url = urllib.unquote(url_desc_map[u"stream"][0])

                        if url_desc_map.has_key(u"sig"):
                                url = url + u"&signature=" + url_desc_map[u"sig"][0]
                        links[key] = url
                highResoVid=selectVideoQuality(links)
                return highResoVid    

				
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
