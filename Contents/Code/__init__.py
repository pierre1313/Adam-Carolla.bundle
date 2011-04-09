import re
from BeautifulSoup import BeautifulStoneSoup as BSS

AC_PREFIX = '/music/adamcarolla'
AC_FEED   = 'http://feeds.feedburner.com/TheAdamCarollaPodcast?format=xml'
#AC_FEED   = 'http://www.adamcarolla.com/ACPBlog/feed/'
AC_NS     = { 'c':'http://purl.org/rss/1.0/modules/content/'}
MRSS      = { 'media':'http://search.yahoo.com/mrss/'}

CACHE_INTERVAL = 3600*1

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(AC_PREFIX, MainMenu, 'Adam Carolla', 'icon-default.jpg', 'art-default.jpg')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'Adam Carolla'
  MediaContainer.content = 'Items'
  MediaContainer.art = R('art-default.jpg')
  HTTP.CacheTime = CACHE_INTERVAL

####################################################################################################
def UpdateCache():
  HTTP.Request(AC_FEED)
  
####################################################################################################
def MainMenu():
  dir = MediaContainer(filelabel='%T')

  for post in XML.ElementFromURL(AC_FEED).xpath('//item'):
    title = post.find('title').text
    match = re.search('[0-9]+\.[0-9]+\.[0-9]+', title)
    if match:
      title = title[match.end(0):].strip()
    
    enc = post.find('enclosure')
    if enc is not None:
      duration = int(enc.get('length'))/12000*1000
      summary = post.find('description').text
      soup = BSS(summary, convertEntities=BSS.XML_ENTITIES) 
      summary = soup.contents[0]
      subtitle = Datetime.ParseDate(post.find('pubDate').text).strftime('%a %b %d, %Y')
      try:
        thumb = post.xpath('media:thumbnail', namespaces=MRSS)[0].get('url')
      except:
        thumb = R('icon-default.jpg')

      dir.Append(TrackItem(enc.get('url'), title, 'Adam Carolla', 'Carolla Radio', summary=summary, subtitle=subtitle, duration=duration, length=enc.get('length'), thumb=thumb))

  return dir
  