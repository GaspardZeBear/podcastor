#!/usr/bin/python
import xml.etree.cElementTree as ET
import urllib2
import re
import sys
import os
import argparse
import requests

urls=[['','http://radiofrance-podcast.net/podcast09/rss_10351.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_14486.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_11495.xml'],
      #['','http://cdn1-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/qui-vive.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_14007.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_10467.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_11921.xml'],
      #['','http://www.rtl.fr/podcast/100-live.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_10078.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_10177.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_12360.xml'],
      #[ 'boomerang', 'http://radiofrance-podcast.net/podcast09/rss_13937.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_16173.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_13397.xml'],
      #['','http://www.bbc.co.uk/programmes/p02pc9zn/episodes/downloads.rss'],
      #['','http://www.bbc.co.uk/programmes/b006qy05/episodes/downloads.rss'],
      ['','http://radiofrance-podcast.net/podcast09/rss_13954.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_16274.xml'],
      #['','http://radiofrance-podcast.net/podcast09/rss_13957.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_10084.xml'],
      #['methode scientifique',  'http://radiofrance-podcast.net/podcast09/rss_14312.xml'],
      #['soft power ', 'http://radiofrance-podcast.net/podcast09/rss_10183.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_17360.xml'],
      #['','http://radiofrance-podcast.net/podcast09/rss_17417.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_10175.xml'],
      #['','http://cdn2-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/mediapolis.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_16119.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_13983.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_10081.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_13956.xml'],
      #[ 'bande originale', 'http://radiofrance-podcast.net/podcast09/rss_13939.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_16408.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_18755.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_18723.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_11701.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_13915.xml'],
       #['','http://radiofrance-podcast.net/podcast09/rss_18148.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_18064.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_18918.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_15537.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_10471.xml'],
      #['','http://radiofrance-podcast.net/podcast09/rss_12526.xml'],
      #['','http://cdn1-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/chapelle-sixties.xml'],
      #['','http://radiofrance-podcast.net/podcast09/rss_19056.xml'],
      #['','http://radiofrance-podcast.net/podcast09/rss_18938.xml'],
      #['','http://podcasts.files.bbci.co.uk/b006qy05.rss'],
      ['','http://radiofrance-podcast.net/podcast09/rss_13022.xml'],
      #['','http://radiofrance-podcast.net/podcast09/rss_10081.xml'],
      #['','http://radiofrance-podcast.net/podcast09/rss_19918.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_16538.xml'],
      #['','https://www.arteradio.com/xml_sound_emission?emissionname=%22SEX%20AND%20SOUNDS%22'],
      #['','https://www.arteradio.com/xml_sound_serie?seriename=%22La%20petite%20g%C3%A2terie%20de%20l%27%C3%A9volution%22'],
      #['','https://www.arteradio.com/xml_sound_serie?seriename=%22MON%20PRINCE%20%20VIENDRA%20A%20LA%20MER%22'],
      #['','https://www.arteradio.com/xml_sound_serie?seriename=%22CENT%20FA%C3%87ONS%20DE%20DISPARA%C3%8ETRE%22'],
      ['','http://radiofrance-podcast.net/podcast09/rss_11550.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_16740.xml'],
      ['','https://www.outilsdumanager.com/feed/podcasts/'],
      ['','http://radiofrance-podcast.net/podcast09/rss_16274.xml'],
      #['a la hussarde',  'http://radiofrance-podcast.net/podcast09/rss_18938.xml'],
      #['femme puissante',  'http://radiofrance-podcast.net/podcast09/rss_20102.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_12440.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_13940.xml'],
      ['','http://radiofrance-podcast.net/podcast09/rss_18292.xml'],
      ['','https://radiofrance-podcast.net/podcast09/rss_20015.xml'],
      ['','https://feed.podbean.com/dissidentofficiel/feed.xml'],
      ['','https://www.rtl.fr/podcast/ca-va-beaucoup-mieux.xml'],
      ['','https://radiofrance-podcast.net/podcast09/rss_14726.xml'],
      ['','https://feed.ausha.co/oLj1PHZx8QPW'],
      ['','https://radiofrance-podcast.net/podcast09/rss_13954.xml'],
      ['','https://radiofrance-podcast.net/podcast09/rss_10239.xml'],
      ['','https://www.europe1.fr/rss/podcasts/la-voix-est-livre.xml']

      ]
content=[]
            
#----------------------------------------------------------------
def getNum(text) :
  part=re.search('\(\d+/\d+\)',text)
  if part is None :
    part=re.search('\d+/\d+',text)
  return part

#----------------------------------------------------------------
def documentInfo(url) :
    #tree = ET.ElementTree(file=urllib2.urlopen(url))
    tree = ET.ElementTree(file=open(cached(url2file(url))))
    root=tree.getroot()
    el=tree.iter(tag='channel').next()
    title=el.find('title').text.encode('ascii',errors='replace')
    link=el.find('link').text.encode('utf-8')
    return(title + ':' + link)

#----------------------------------------------------------------
def url2file(url) :
    file=url
    #file=re.sub(':','_',url)
    file=re.sub('\/','@',file)
    return(file)

#----------------------------------------------------------------
def documentsInfo(filter) :
  for i in range(0,len(urls)) :
    text=documentInfo(urls[i][1])
    if re.search(filter,text) is None :
      continue
    #print("{:3} {:<60.60} {}".format(str(i),documentInfo(urls[i]),urls[i]))
    print("{:3} {:<80.80} {}".format(str(i),documentInfo(urls[i][1]),urls[i][1]))

#----------------------------------------------------------------
def cached(file) :
    return("cache/" + file)
    
#----------------------------------------------------------------
def XdocumentCache(url) :
  print("Loading file " + url)
  file=urllib2.urlopen(url)
  print("Caching file " + url)
  with open(cached(url2file(url)),'w') as out : 
    out.write(file.read())
    
#----------------------------------------------------------------
def documentCache(url) :
  print("Loading file " + url)
  r=requests.get(url)
  print("Caching file " + url)
  #print(r.content)
  with open(cached(url2file(url)),'w') as out : 
    out.write(r.content)

#----------------------------------------------------------------
def documentsCache() :
  #for i in range(1,len(urls)-1) :
  for i in range(0,len(urls)) :
    print("Prepare caching file " + urls[i][1] + " " + str(i+1) + "/" + str(len(urls)))
    documentCache(urls[i][1])

#----------------------------------------------------------------
def rss(url,filter,prefix,download) :
  #tree = ET.ElementTree(file=urllib2.urlopen(url))
  tree = ET.ElementTree(file=open(cached(url2file(url))))
  root=tree.getroot()
  count=0
  for el in tree.iter(tag='item') :
    text=el.find('title').text.encode('utf-8')
    if re.search(filter,text) is None :
      continue
    count += 1
  #count=0
  print(documentInfo(url))
  for el in tree.iter(tag='item') :
    text=el.find('title').text.encode('utf-8')
    pubDate=el.find('pubDate').text.encode('utf-8')
    mp3=el.find('enclosure').attrib['url']
    if re.search(filter,text) is None :
      continue
    part=getNum(text)
    #sPart=str(count)
    sPart='{:02d}'.format(count)
    if part :
      sPart=part.group()
      sPart=re.sub('\(','',sPart)
      sPart=re.sub('\)','',sPart)
      sPart=re.sub('/','-',sPart)
    else :
      count -= 1
    file=prefix + '_' + sPart + '.mp3'
    #content.append('{:<16.16} {:<100.100} wget -O {:s} {:s}'.format(pubDate,text, file, mp3 ))
    #content.append('{:<16.16} {:_<100.100} wget -O {:s} {:s}'.format(pubDate,text.decode('utf8').encode('utf8',errors='replace'), file, mp3 ))
    #textNorm=unicode(text.decode('utf8').encode('utf8',errors='replace').encode("utf-8")[:80], "utf-8", errors="ignore")
    textNorm=text.decode('utf8').encode('ascii',errors='replace')
    content.append('{:<16.16} {:_<80.80} {:s}'.format(pubDate,textNorm, mp3 ))

    if download :
      cmd='/usr/bin/wget -O ' + file + ' ' + mp3
      print(cmd)
      os.system("nohup " + cmd + "> /dev/null 2>&1 &")
  for item in reversed(content) :
    print(item)

#----------------------------------------------------------------
def fList(args=None) :
  filter='.*'
  if args.filter :
    filter=args.filter[0]
  documentsInfo(filter)

#----------------------------------------------------------------
def fCache(args=None) :
  if args.num :
    for n in args.num.split(',') :
      documentCache(urls[int(n)][1])    
  else :
    documentsCache()
   
#----------------------------------------------------------------
def fScan(args) :
  url=urls[int(args.item)][1]
  filter='.*'
  if args.filter :
    filter=args.filter[0]
  prefix='podcast'
  if args.prefix :
    prefix=args.prefix[0]
  rss(url,filter,prefix,args.download) 
  
#----------------------------------------------------------------
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')

parserList = subparsers.add_parser('list', help='a help')
parserList.set_defaults(func=fList)
parserList.add_argument('--filter','-f',nargs=1,help="filter for scan")


parserCache = subparsers.add_parser('cache', help='a help')
parserCache.set_defaults(func=fCache)
parserCache.add_argument('num',nargs='?',help="num of file to cache")

parserScan = subparsers.add_parser('scan', help='a help')
parserScan.set_defaults(func=fScan)
parserScan.add_argument('item',nargs='?',help="item to scan (given by list)")
parserScan.add_argument('--filter','-f',nargs=1,help="filter for scan")
parserScan.add_argument('--prefix','-p',nargs=1,help="prefix for filename")
parserScan.add_argument('--download','-d',help="download",action="store_true")

args=parser.parse_args()
args.func(args)
