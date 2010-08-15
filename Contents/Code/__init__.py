import re
from BeautifulSoup import BeautifulStoneSoup as BSS

AC_PREFIX = '/music/adamcarolla'
AC_FEED   = 'http://www.adamcarolla.com/ACPBlog/feed/'
AC_NS     = { 'c':'http://purl.org/rss/1.0/modules/content/'}

CACHE_INTERVAL = 3600*1

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(AC_PREFIX, MainMenu, 'Adam Carolla', 'icon-default.jpg', 'art-default.jpg')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'Adam Carolla'
  MediaContainer.content = 'Items'
  MediaContainer.art = R('art-default.jpg')
  HTTP.SetCacheTime(CACHE_INTERVAL)

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
      duration = int(enc.get('length'))/8000*1000
      summary = post.find('description').text
      soup = BSS(summary, convertEntities=BSS.XML_ENTITIES) 
      summary = soup.contents[0]
      subtitle = Datetime.ParseDate(post.find('pubDate').text).strftime('%a %b %d, %Y')
    
      desc = XML.ElementFromString(post.xpath('c:encoded', namespaces=AC_NS)[0].text, True)
      images = desc.xpath('//img')
      thumb = None
      for img in images:
        src = img.get('src')
        if src.find('podtrac') == -1:
          thumb = src
          break
    
      dir.Append(TrackItem(enc.get('url'), title, 'Adam Carolla', 'Carolla Radio', summary=summary, subtitle=subtitle, duration=duration, length=enc.get('length'), thumb=thumb))

  return dir
  