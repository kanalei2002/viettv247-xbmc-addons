import os
import string
import sys
import re
import urlresolver
import xbmc, xbmcaddon, xbmcplugin, xbmcgui

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

from metahandler import metahandlers

addon_id='plugin.video.kamerdb'
addon = Addon(addon_id, sys.argv)
version = '1.0.0'

net = Net()

#Common Cache
import xbmcvfs
dbg = False # Set to false if you don't want debugging

#Common Cache
try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer('plugin.video.kamerdb')

################### Global Constants #################################

#URLS
BASEURL = 'http://www.merdb.ru'
CONTENTURL = 'http://www.merdb.ru'

#PATHS
AddonPath = addon.get_path()
IconPath = os.path.join(AddonPath, 'icons')

from universal import _common as univ_common        
from universal import favorites, watchhistory
#fav = favorites.Favorites(addon_id, sys.argv)

#VARIABLES
VideoType_Movies = 'movie'
VideoType_TV = 'tvshow'
VideoType_Season = 'season'
VideoType_Episode = 'episode'
VideoType_Link = 'link'

play = addon.queries.get('play', '')    
mode = addon.queries['mode']
url = addon.queries.get('url', '')
title = addon.queries.get('title', '')
img = addon.queries.get('img', '')
fanart = addon.queries.get('fanart', '')
section = addon.queries.get('section', '')
page = addon.queries.get('page', '')
video_type = addon.queries.get('video_type', '')
name = addon.queries.get('name', '')
imdb_id = addon.queries.get('imdb_id', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
historytitle = addon.queries.get('historytitle', '')
historylink = addon.queries.get('historylink', '')
iswatchhistory = addon.queries.get('watchhistory', '')
year = addon.queries.get('year', '')
show = addon.queries.get('show', '')
queued = addon.queries.get('queued', '')

items_per_page = 25

#################### Addon Settings ##################################

#Helper function to convert strings to boolean values
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
  
meta_setting = str2bool(addon.get_setting('use-meta'))

metaget=metahandlers.MetaData()

def WatchedCallback():    
    metaget.change_watched(video_type, show, imdb_id, season=season, episode=episode, year=year, watched=7)    
    xbmc.executebuiltin("Container.Refresh")

#################### Helper Functions ##################################

def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\r": "",            
                   "\n": "",
                   "\t": "",   
                   "%3a": ":",
                   "%3A":":",
                   "%2f":"/",
                   "%2F":"/",
                   "%3f":"?",
                   "%3F":"?",
                   "%26":"&",
                   "%3d":"=",
                   "%3D":"=",
                   "%2C":",",
                   "%2c":","
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text
        
def Notify(typeq, title, message, times, line2='', line3=''):
     if title == '':
          title='B-Movies'
     if typeq == 'small':
          if times == '':
               times='5000'
          smallicon= os.path.join(IconPath, 'icon.png')
          xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+smallicon+")")
     elif typeq == 'big':
          dialog = xbmcgui.Dialog()
          dialog.ok(' '+title+' ', ' '+message+' ', line2, line3)
     else:
          dialog = xbmcgui.Dialog()
          dialog.ok(' '+title+' ', ' '+message+' ')
		
def add_video_directory(mode, video_type, link, vidtitle, vidname, imdb='', year='', season_num=0, totalitems=0, favourite=False, img=''):

    meta = get_metadata(video_type, vidtitle, year=year, imdb=imdb, season_num=season_num, img=img)
    contextMenuItems = add_contextmenu(meta_setting, video_type, link, vidtitle, vidname, favourite, watched=meta['overlay'], imdb=meta['imdb_id'], year=year, season_num=season_num, img=img)
    
    fav_sub_section_title = ''
    fav_title = ''
    fav_context_menu_index = 0
    if video_type == VideoType_Season:
        fav_context_menu_index = 0
        fav_sub_section_title = 'Seasons'
        fav_title = vidtitle + ' - Season: ' + str(season_num)
        if favourite:
            meta['title'] = vidtitle + ' - Season: ' + str(season_num)
        else:
            meta['title'] = 'Season-' + str(season_num)        
    else:
        fav_context_menu_index = 1
        fav_sub_section_title = 'Shows'
        fav_title = vidname
        meta['title'] = vidname
    
    infolabels = {'supports_meta' : 'true', 'video_type' : video_type, 'name' : vidtitle, 'imdb_id' : imdb, 'year' : year, 'season' : season_num}
    queries = {'mode': mode, 'url': link, 'video_type': VideoType_Season, 'imdb_id': meta['imdb_id'], 'show' : vidtitle, 'title': vidtitle, 'name': vidname, 'season': season_num, 'img': meta['cover_url'], 'fanart': meta['backdrop_url']}

    addon.add_directory(queries, meta, contextMenuItems, context_replace=True, img=img, fanart=meta['backdrop_url'], total_items=totalitems)


def add_video_item(video_type, section, link, vidtitle, vidname, year='', imdb='', season_num=0, episode_num=0, totalitems=0, favourite=False, img='', add_as_dir=True):

    meta = get_metadata(video_type, vidtitle, vidname, year, imdb=imdb, season_num=season_num, episode_num=episode_num, img=img)
    if video_type == VideoType_Movies:
        contextMenuItems = add_contextmenu(meta_setting, video_type, link, univ_common.str_conv(addon.decode(vidtitle)), meta['title'], favourite, watched=meta['overlay'], imdb=meta['imdb_id'], year=meta['year'], img=img)
        #contextMenuItems = add_contextmenu(meta_setting, video_type, link, univ_common.str_conv(addon.decode(vidtitle)), vidtitle, favourite,  imdb=imdb, year=year, img=img)
    else:
        contextMenuItems = add_contextmenu(meta_setting, video_type, link, univ_common.str_conv(addon.decode(vidtitle)), meta['title'], favourite, watched=meta['overlay'], imdb=meta['imdb_id'], season_num=season_num, episode_num=episode_num, img=img)
    
    if video_type == VideoType_Movies:
        infolabels = {'supports_meta' : 'true', 'video_type' : video_type, 'name' : vidtitle, 'imdb_id' : meta['imdb_id'], 'year' : meta['year']}
        queries = {'url': link, 'video_type': video_type, 'imdb_id': meta['imdb_id'], 'title': vidtitle, 'name': vidname, 'year': meta['year'], 'img': meta['cover_url'], 'fanart': meta['backdrop_url']}
        
        if add_as_dir == True:  
            queries['mode'] = 'links'            
        else:
            queries['play'] = 'true'

        addon.add_directory(queries, meta, contextMenuItems, context_replace=True, img=img, fanart=meta['backdrop_url'], total_items=totalitems)
    elif video_type == VideoType_Episode:
      
        video_title = ''        
        season_episode = 's' + str(season_num) + 'e' + str(episode_num)
        meta_season_episode = 'Episode: ' + str(episode_num)        
        fav_season_episode = 'Season: ' + str(season_num) + ' Episode: ' + str(episode_num)        
        if meta_setting:
            favpretitle = vidtitle + ' - ' + fav_season_episode
            pretitle = vidtitle + ' - ' + season_episode
            meta_pretitle = meta_season_episode
            if meta['title']:
                fav_video_title = favpretitle + ' - ' + meta['title']
                video_title = pretitle + ' - ' + meta['title']
                meta['title'] = meta_pretitle + ' - ' + meta['title']
            else:
                fav_video_title = favpretitle
                video_title = pretitle
                meta['title'] = meta_pretitle
        else:
            fav_video_title = meta['title'] + ' - ' + fav_season_episode
            video_title = meta['title'] + ' - ' + season_episode
            meta['title'] = meta_season_episode
            
        if favourite:
            meta['title'] = fav_video_title
        
        infolabels = {'supports_meta' : 'true', 'video_type' : video_type, 'name' : vidtitle, 'imdb_id' : meta['imdb_id'], 'season': season_num, 'episode' : episode_num}
        queries = {'url': link, 'video_type': video_type, 'imdb_id': meta['imdb_id'], 'show' : vidtitle, 'title': video_title, 'name': vidname, 'season': season_num, 'episode' : episode_num, 'img': meta['cover_url'], 'fanart': meta['backdrop_url']}
        if add_as_dir == True:
            queries['mode'] = 'links'            
        else:
            queries['play'] = 'true'
        #p_url = fav.build_url(queries)
        #contextMenuItems.insert(1, ('Add to Favorites', fav.add_directory(fav_video_title, p_url, section_title='TV', sub_section_title='Episodes', img=meta['cover_url'], fanart=meta['backdrop_url'], infolabels=infolabels)))
        addon.add_directory(queries, meta, contextMenuItems, context_replace=True, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=totalitems)

def add_video_link(video_type, link, vidtitle, vidname, img='', fanart='', totalitems=0):
    
    contextMenuItems = add_contextmenu(False, VideoType_Link, link, vidtitle, vidtitle, False)            
    queries = {'play' : 'true', 'url': link, 'video_type': video_type, 'imdb_id': imdb_id, 'show' : show, 'title': vidtitle, 'name': vidname, 'year' : year, 'img': img, 'fanart' : fanart, 'season' : season, 'episode' : episode, 'historytitle' : vidtitle, 'historylink' : sys.argv[0]+sys.argv[2]}    
    
    from universal import playbackengine    
    contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, vidtitle, addon.build_plugin_url( queries ) ) ) )
    
    addon.add_directory(queries, {'title' : vidname}, contextMenuItems, context_replace=False, img=img, fanart=fanart, total_items=totalitems)
    
def setView(content, viewType):
    
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )
    
    # set sort methods - probably we don't need all of them
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )        
    
#################### Meta-Data related functions ##################################

def refresh_movie(vidtitle, year=''):

    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()
        
    search_meta = metaget.search_movies(vidtitle)
    
    if search_meta:
        movie_list = []
        for movie in search_meta:
            movie_list.append(movie['title'] + ' (' + str(movie['year']) + ')')
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose', movie_list)
        
        if index > -1:
            new_imdb_id = search_meta[index]['imdb_id']
            new_tmdb_id = search_meta[index]['tmdb_id']       
            meta = metaget.update_meta('movie', vidtitle, imdb_id=imdb_id, new_imdb_id=new_imdb_id, new_tmdb_id=new_tmdb_id, year=year)   
            xbmc.executebuiltin("Container.Refresh")
    else:
        msg = ['No matches found']
        addon.show_ok_dialog(msg, 'Refresh Results')


def episode_refresh(vidname, imdb, season_num, episode_num):
    #refresh info for an episode   
    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()
        
    metaget.update_episode_meta(vidname, imdb, season_num, episode_num)
    xbmc.executebuiltin("XBMC.Container.Refresh")


def season_refresh(vidname, imdb, season_num):

    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()          	
        
    metaget.update_season(vidname, imdb, season_num)
    xbmc.executebuiltin("XBMC.Container.Refresh")

def get_metadata(video_type, vidtitle, vidname='', year='', imdb='', season_list=None, season_num=0, episode_num=0, img=''):    
    meta = {}
    
    if meta_setting:
        #Get Meta settings
        poster = addon.get_setting('movie-poster')
        fanart = addon.get_setting('movie-fanart')
        
        if video_type in (VideoType_Movies, VideoType_TV):
            print video_type + vidtitle + year 
            meta = metaget.get_meta(video_type, vidname,'',None, year,overlay=6)
            
        returnlist = True
        if video_type == VideoType_Season:            
            if not season_list:
                season_list = []
                season_list.append(season_num)
                returnlist = False
            meta = metaget.get_seasons(vidtitle, imdb, season_list)
            if not returnlist:
                meta = meta[0]
    
        if video_type == VideoType_Episode:
            meta=metaget.get_episode_meta(vidname, imdb, season_num, episode_num)
        
        if not returnlist:
            #Check for and blank out covers if option disabled
            if poster == 'false':
                meta['cover_url'] = ''                    
            #Check for and blank out fanart if option disabled
            if fanart == 'false':
                meta['backdrop_url'] = ''        
            if meta.get('title', '') == '':
                meta['title'] = vidname
            if meta.get('cover_url', '') == '':
                meta['cover_url'] = img
            if meta.get('imdb_id', '') == '':
                meta['imdb_id'] = imdb
            if meta.get('backdrop_url', '') == '':
                meta['backdrop_url'] = ''
            if meta.get('year', '') == '':
                meta['year'] = year
            if meta.get('overlay', '') == '':
                meta['overlay'] = 0
        
    else:
        
        meta['title'] = vidname
        meta['cover_url'] = img
        meta['imdb_id'] = imdb
        meta['backdrop_url'] = ''
        meta['year'] = year
        meta['overlay'] = 0
        if video_type in (VideoType_TV, VideoType_Episode):
            meta['TVShowTitle'] = vidtitle                    

    return meta

    
#################### Context-Menu related functions ##################################

def add_contextmenu(use_meta, video_type, link, vidtitle, vidname, favourite, watched='', imdb='', year='', season_num=0, episode_num=0, img=''):
    
    contextMenuItems = []
    
    if video_type == VideoType_Link:
        return contextMenuItems
    
    if video_type in (VideoType_Movies, VideoType_Episode, VideoType_TV):
        contextMenuItems.append(('Show Information', 'XBMC.Action(Info)'))

    #Meta is turned on so enable extra context menu options
    if use_meta:
        if watched == 6:
            watched_mark = 'Mark as Watched'
        else:
            watched_mark = 'Mark as Unwatched'

        contextMenuItems.append((watched_mark, 'XBMC.RunPlugin(%s?mode=watch_mark&video_type=%s&title=%s&imdb_id=%s&season=%s&episode=%s)' % (sys.argv[0], video_type, vidtitle, imdb, season_num, episode_num)))
        contextMenuItems.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=refresh_meta&video_type=%s&title=%s&year=%s&season=%s&episode=%s)' % (sys.argv[0], video_type, vidtitle, year, season_num, episode_num)))
        
        #if video_type == VideoType_Movies:
            #contextMenuItems.append(('Search for trailer', 'XBMC.RunPlugin(%s?mode=trailer_search&vidname=%s&url=%s)' % (sys.argv[0], title, link)))                        

    return contextMenuItems
    

#################### Main Functions ##################################        
def MainMenu():    
    
    addon.add_directory({'mode': 'menu', 'url' : CONTENTURL , 'video_type' : VideoType_Movies }, {'title': 'Movies'}, img=os.path.join(IconPath, 'movies.png'))       
    addon.add_directory({'mode': 'menu', 'url' : CONTENTURL + '/tvshow', 'video_type' : VideoType_TV }, {'title': 'TV Shows'}, img=os.path.join(IconPath, 'tvshows.png'))       
    #fav.add_my_fav_directory(img=os.path.join(IconPath, 'favorites.png'))
    addon.add_directory({'mode': 'resolver'}, {'title':  'Resolver Settings'}, img=os.path.join(IconPath, 'resolver.png'))               
    
    setView(None, 'default-view')

def GenerateMenu(menu_items):
    for (title, section, page, icon, mode) in menu_items:
        addon.add_directory({'mode': mode, 'url' : url, 'section' : section, 'page' : page, 'video_type' : video_type }, {'title': title}, img=os.path.join(IconPath, icon))       
    
    setView(None, 'default-view')
    
menu_items = [ 
    ('All', '', '0', 'all.png', 'browse'),
    ('Genre', '', '', 'genre.png', 'genre'),
    ('Featured', '/?featured=1&sort=stamp', '0', 'featured.png', 'browse'),
    ('Ratings', '/?sort=ratingp', '', 'ratings.png', 'browse'),   
    ('Popular', '/?sort=views', '0', 'popular.png', 'browse'),
    ('Favorites', '/?sort=favorite', '0', 'favorites.png', 'browse'),
    ('Release Date', '/?sort=year', '0', 'releasedate.png', 'browse'),
    ('Date Added', '/?sort=stamp', '0', 'dateadded.png', 'browse'),
    ('Search', '', '', 'search.png', 'search')
    ]    
def Menu():

    GenerateMenu(menu_items)

    setView(None, 'default-view')
    
def AtoZ():
        
    az_menu_items = []
    az_url = BASEURL
    if 'movie' in url:
        az_url = az_url + '/movies'
    else:
        az_url = az_url + '/tv-show'
        
    az_content = net.http_GET(az_url).content
    genre_content = addon.unescape(az_content)
    az_content = unescape(az_content)
    for az in re.finditer(r"<a href=\"\?startwith=(.+?)\">(.+?)</a>", az_content):
        az_menu_items.append((az.group(2).strip(), 'startwith=' + az.group(1), '0', '', 'browse'))
        
    GenerateMenu(az_menu_items)
    setView(None, 'default-view')
    
def Genre():
        
    genre_menu_items = []
    genre_url = BASEURL
    if 'tvshow' in url:
        genre_url = genre_url + '/index.php'
    else:
        genre_url = genre_url + '/index.php'
        
    #print 'genre url ' + genre_url   
    genre_content = net.http_GET(genre_url).content
    genre_content = addon.unescape(genre_content)
    genre_content = unescape(genre_content)
    genre_content = genre_content.replace('<li><a href="/?genre=" title="Watch  Movies"></a></li><li class="divider"></li>','').replace('<li><a href="/tvshow/?genre=" title="Watch  TVShows"></a></li>','')
    #print genre_content
    genre_content = re.compile('<ul class="dropdown-menu">(.+?)</ul>').findall(genre_content)
    #genre_content = genre_content.replace('<li><a href="/?genre=" title="Watch  Movies"></a></li><li class="divider"></li>','')
    #print genre_content
    genre_content1 = re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a></li>').findall(genre_content[0])
    #print genre_content1
    for url1, name in genre_content1:
        genre_menu_items.append((name, url1, '1', '', 'browse'))
        #print name + ' ' + url1
            
    GenerateMenu(genre_menu_items)
    setView(None, 'default-view')
        
def Browse(url):    
    #url = 'http://www.merdb.ru/?genre=Action'
     
    browse_url = url
    #print 'url in browse' + browse_url
   # print 'section in browse ' +  section
    if(browse_url == 'http://www.merdb.ru'):
        if section:
            browse_url = BASEURL + section
    if(browse_url == 'http://www.merdb.ru/tvshow'):
        if section:
            browse_url = url + section
      
    #print 'browse_url ' + browse_url
    content = net.http_GET(browse_url).content
    content = addon.unescape(content)
    content = unescape(content)
    if video_type == VideoType_Movies:
        try:
            content = content.decode("ISO-8859-1")
            content =content.encode("UTF-8")
        except: pass
    elif video_type == VideoType_TV:
        try:
            content = content.decode("ascii", 'ignore')
            content =content.encode("UTF-8")
        except: pass
    #print 'content in browse '+content
    
    movies = re.compile('<div class="main_list_box"><a href=".+?" title="(.+?)"><img src="(.+?)" class="main_list_picsize" alt=".+?"/></a><div class="list_box_title"><a href="(.+?)" title=".+?">(.+?)</a></div>').findall(content)
   
    for  movie_title, movie_img, movie_url, movie_title1 in movies:
        movie_year = ''
        if video_type == VideoType_Movies:
            movie_title_year = movie_title.split('(')
            movie_year = movie_title_year[1].replace(')','')
            movie_title = movie_title_year[0].replace('Watch ','')
            #print movie_title + ' ' + VideoType_Movies + ' ' + movie_year
            add_video_item(video_type, video_type, movie_url, movie_title.strip(), movie_title.strip(), year=movie_year, totalitems=len(movies), img=movie_img, add_as_dir=True)
        elif video_type == VideoType_TV:
            movie_title_year = movie_title1.split('(')
            movie_year = movie_title_year[1].replace(')','')
            #print movie_title + ' ' + VideoType_Movies + ' ' + movie_year
            add_video_directory('tvseasons', video_type, movie_url, movie_title.strip(), movie_title.strip(), year=movie_year, totalitems=len(movies), img=movie_img)
           
    paginate=re.compile('<li class="active"><span class="currentpage">.+?</span></li><li><a href="(.+?)">.+?</a></li>').findall(content)
    #print paginate
    
    #if movie_count >= items_per_page:
    if paginate:
        if video_type == VideoType_Movies:
            addon.add_directory({'mode': 'browse', 'url' : BASEURL+'/'+paginate[0], 'video_type' : video_type }, {'title': 'Next Page >>'} )
        elif video_type == VideoType_TV:
            addon.add_directory({'mode': 'browse', 'url' : BASEURL+'/tvshow/'+paginate[0], 'video_type' : video_type }, {'title': 'Next Page >>'} )
        
    
    content_type = None
    view_setting_id = 'default-view'
    if video_type == VideoType_Movies:
        content_type = 'movies'
        view_setting_id = 'movie-view'
    elif video_type == VideoType_TV:
        content_type = 'tvshows'
        view_setting_id = 'tvshow-view'
    setView(content_type, view_setting_id)
    

def GetTVSeasons(url):

    url = BASEURL + url
    print 'URL GETTVseason' + url
    tv_content = net.http_GET(url).content
  
    tv_seasons = re.compile("Season.*?([0-9]+?)</a></h2>").findall(tv_content)
    for season_num in tv_seasons:
        add_video_directory('tvepisodes', video_type, url, title, 'Season: ' + str(int(season_num)), season_num=str(int(season_num)) ,imdb=imdb_id, totalitems=len(tv_seasons), img=img)
        
    setView('seasons', 'season-view')    

def GetTVEpisodes(url):

    tv_content = net.http_GET(url).content
    try:
        tv_content = tv_content.decode("ascii", 'ignore')
        tv_content = tv_content.encode("UTF-8")
    except: pass
    tv_content = addon.unescape(tv_content)
    tv_content = unescape(tv_content)
    

    tv = re.compile('<div class="actual_tab" id="first">(.+?)</div></div><div class="movie_box">').findall(tv_content)

    tv_seasons = re.compile('<h2><a href="(.+?)">Season.*?([0-9]+?)</a></h2>').findall(tv[0])

    for season_url, season_num in tv_seasons:
      if (season_num == season):
          tv_season_episodes_list = re.compile('<a href="'+season_url+'-(.+?)">.+? </a>').findall(tv[0])
    
          for episode_num in tv_season_episodes_list:
              number = episode_num.split('-')
              add_video_item(VideoType_Episode, VideoType_Episode, season_url+'-'+episode_num, title, title, season_num=int(season), episode_num=int(number[1]), imdb=imdb_id, totalitems=len(episode), img=img, add_as_dir=True)                
            
    setView('episodes', 'episode-view')    
        
def GetLinks(url):
  
    url = BASEURL + '/' + url
    movie_content = net.http_GET(url).content
    
    movie_content = addon.unescape(movie_content)
    movie_content = unescape(movie_content)
    #movie_content = re.sub("\\\"", "\"", movie_content)
    try:
        movie_content = movie_content.decode("ISO-8859-1")
        movie_content= movie_content.encode("UTF-8")
    except: pass
    from universal import _common as univ_common
    movie_content = univ_common.str_conv(addon.decode(movie_content)).replace('              ','').replace('            ','').replace('          ','').replace('    ','').replace('  ','')
    
    container_pattern = r'<table[^>]+class="movie_version[ "][^>]*>(.*?)</table>'
    item_pattern = (
        r'quality_(?!sponsored|unknown)([^>]*)></span>.*?'
        r'url=([^&]+)&(?:amp;)?domain=([^&]+)&(?:amp;)?(.*?)'
        r'"version_veiws"> ([\d]+) views</')

    for version in re.finditer(container_pattern, movie_content, re.DOTALL | re.IGNORECASE):
        for source in re.finditer(item_pattern, version.group(1), re.DOTALL):
            link_quality, link_url, link_title, link_parts, link_views = source.groups()
            
            host = link_title.decode('base-64').lower()        
            hosted_media = urlresolver.HostedMediaFile(host=host, media_id='DUMMY')
            if hosted_media:
              #add_video_link(video_type, link_url.decode('base-64'), title, '[COLOR pink]' + title + '[/COLOR] [COLOR red][' + link_quality.upper() + '][/COLOR] [COLOR yellow]: ' +  link_title.decode('base-64').upper() + '[/COLOR] (' + link_views + ' views)', img=img, fanart=fanart, totalitems= len(source.groups()) )
              add_video_link(video_type, link_url.decode('base-64'), title, '[COLOR pink]' + title + '[/COLOR] [COLOR red][' + link_quality.upper() + '][/COLOR] [COLOR yellow]: ' +  link_title.decode('base-64').upper() + '[/COLOR]', img=img, fanart=fanart, totalitems= len(source.groups()) )

def Search(url):

    print 'search ' + url
    try:
        keyboard = xbmc.Keyboard()
        keyboard.setHeading('Search')
        #keyboard.setDefault(last_search)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            searchText = keyboard.getText()
            addon.save_data('search',searchText)
  
        browse_url = url+'/?search='+searchText
        
        if(searchText != ''):
            content = net.http_GET(browse_url).content
            content = addon.unescape(content)
            content = unescape(content)
            if video_type == VideoType_Movies:
                try:
                    content = content.decode("ISO-8859-1")
                    content =content.encode("UTF-8")
                except: pass
            elif video_type == VideoType_TV:
                try:
                    content = content.decode("ascii", 'ignore')
                    content =content.encode("UTF-8")
                except: pass
            #print 'content in browse '+content
    
            movies = re.compile('<div class="main_list_box"><a href=".+?" title="(.+?)"><img src="(.+?)" class="main_list_picsize" alt=".+?"/></a><div class="list_box_title"><a href="(.+?)" title=".+?">(.+?)</a></div>').findall(content)
            #print movies
            for  movie_title, movie_img, movie_url, movie_title1 in movies:
                movie_year = ''
                if video_type == VideoType_Movies:
                    movie_title_year = movie_title.split('(')
                    movie_year = movie_title_year[1].replace(')','')
                    movie_title = movie_title_year[0].replace('Watch ','')
                   # print movie_title + ' ' + VideoType_Movies + ' ' + movie_year
                    add_video_item(video_type, video_type, movie_url, movie_title.strip(), movie_title.strip(), year=movie_year, totalitems=len(movies), img=movie_img, add_as_dir=True)
                elif video_type == VideoType_TV:
                    movie_title_year = movie_title1.split('(')
                    movie_year = movie_title_year[1].replace(')','')
                   # print movie_title + ' ' + VideoType_Movies + ' ' + movie_year
                    add_video_directory('tvseasons', video_type, movie_url, movie_title.strip(), movie_title.strip(), year=movie_year, totalitems=len(movies), img=movie_img)
           
            paginate=re.compile('<li class="active"><span class="currentpage">.+?</span></li><li><a href="(.+?)">.+?</a></li>').findall(content)

            if paginate:
                if video_type == VideoType_Movies:
                    addon.add_directory({'mode': 'browse', 'url' : BASEURL+'/'+paginate[0], 'video_type' : video_type }, {'title': 'Next Page >>'} )
                elif video_type == VideoType_TV:
                    addon.add_directory({'mode': 'browse', 'url' : BASEURL+'/tvshow/'+paginate[0], 'video_type' : video_type }, {'title': 'Next Page >>'} )

          
    except: pass

    
    content_type = None
    view_setting_id = 'default-view'
    if video_type == VideoType_Movies:
        content_type = 'movies'
        view_setting_id = 'movie-view'
    elif video_type == VideoType_TV:
        content_type = 'tvshows'
        view_setting_id = 'tvshow-view'
    setView(content_type, view_setting_id)
    
def ShowSearchDialog():
    last_search = addon.load_data('search')
    if not last_search: last_search = ''
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Search')
    keyboard.setDefault(last_search)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        query = keyboard.getText()
        addon.save_data('search',query)
        Search(query)
    else:
        return        

        
def Play(url):
    print 'url in play' + url
    from universal import playbackengine
    print 'url in Play' + url + queued
    item_title = title
    display_name = title
    if video_type != VideoType_Movies:
        item_title = show
        
    if queued == 'true':

            hosted_media = urlresolver.HostedMediaFile(url=url)
            if hosted_media:
                resolved_media_url = urlresolver.resolve(url)  
                if resolved_media_url:
                    
                    player = playbackengine.Play(resolved_url=resolved_media_url, addon_id=addon_id, video_type=video_type, 
                                title=item_title,season=season, episode=episode, year=year, watchedCallback=WatchedCallback)
                                
                    '''
                    add to watch history - start
                    '''
                    wh = watchhistory.WatchHistory(addon_id)
                    
                    infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':title, 'imdb_id':imdb_id, 'season':season, 'episode':episode, 'year':year }          
                                        
                    if historylink:
                        wh.add_video_item(display_name + ' - ' + name, sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_playable=True, parent_title=historytitle)
                        wh.add_directory(historytitle, historylink, infolabels=infolabels, img=img, fanart=fanart, level='1')
                    else:
                        wh.add_video_item(display_name + ' - ' + name, sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_playable=True)
                    '''
                    add to watch history - end
                    '''
                    player.KeepAlive()
                                    
    else:
        playbackengine.PlayInPL(display_name, img=img)
        

if play:
    Play(url)
        
if mode == 'main': 
    MainMenu()
elif mode == 'menu':
    Menu()
elif mode == 'az':
    AtoZ()    
elif mode == 'genre':
    Genre()    
elif mode == 'browse':
    Browse(url)
elif mode == 'tvseasons':
    GetTVSeasons(url)
elif mode == 'tvepisodes':
    GetTVEpisodes(url)
elif mode == 'links':
    GetLinks(url)
elif mode == 'search':
    Search(url)
elif mode == 'googlesearch':
    GoogleSearch(url)
elif mode == 'resolver':
    urlresolver.display_settings()
elif mode == 'metahandlersettings':
    import metahandler
    metahandler.display_settings()
elif mode == 'refresh_meta':
    if video_type == VideoType_Movies:
        refresh_movie(title)
    elif video_type == VideoType_TV:
        Notify('small', 'Refresh TV Show', 'Feature not yet implemented','')
    elif video_type == VideoType_Season:
        season_refresh(title, imdb_id, season)
    elif video_type == VideoType_Episode:
        episode_refresh(title, imdb_id, season, episode)
elif mode == 'watch_mark':  
    if not metaget:
        metaget=metahandlers.MetaData()
    addon.log(video_type + ',' + title + ',' + imdb_id + ',' + season + ',' + episode)
    metaget.change_watched(video_type, title, imdb_id, season=season, episode=episode)
        
    xbmc.executebuiltin("Container.Refresh")
elif mode == 'universalsettings':    
    from universal import _common
    _common.addon.show_settings()

if not play and mode != 'resolver' and mode != 'metahandlersettings' and mode != 'universalsettings':
    addon.end_of_directory()
    search_url = ''
