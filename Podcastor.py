#!/usr/bin/python

import xml.etree.cElementTree as ET
import urllib2
import re
import sys
import os
import argparse

urls=['http://radiofrance-podcast.net/podcast09/rss_15537.xml',
      'http://radiofrance-podcast.net/podcast09/rss_10351.xml',
      'http://radiofrance-podcast.net/podcast09/rss_14486.xml',
      'http://radiofrance-podcast.net/podcast09/rss_11495.xml',
      'http://cdn1-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/qui-vive.xml',
      'http://radiofrance-podcast.net/podcast09/rss_14007.xml',
      'http://radiofrance-podcast.net/podcast09/rss_11475.xml',
      'http://radiofrance-podcast.net/podcast09/rss_10467.xml',
      'http://radiofrance-podcast.net/podcast09/rss_11921.xml',
      'http://www.rtl.fr/podcast/100-live.xml',
      'http://radiofrance-podcast.net/podcast09/rss_10192.xml',
      'http://radiofrance-podcast.net/podcast09/rss_10078.xml',
      'http://radiofrance-podcast.net/podcast09/rss_10177.xml',
      'http://radiofrance-podcast.net/podcast09/rss_12360.xml',
      'http://radiofrance-podcast.net/podcast09/rss_13937.xml',
      'http://radiofrance-podcast.net/podcast09/rss_16173.xml',
      'http://radiofrance-podcast.net/podcast09/rss_13397.xml',
      'http://www.bbc.co.uk/programmes/p02pc9zn/episodes/downloads.rss',
      'http://www.bbc.co.uk/programmes/b006qy05/episodes/downloads.rss',
      'http://radiofrance-podcast.net/podcast09/rss_13915.xml',
      'http://radiofrance-podcast.net/podcast09/rss_13954.xml',
      'http://radiofrance-podcast.net/podcast09/rss_16274.xml'
      ]

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
    title=el.find('title').text.encode('utf-8')
    link=el.find('link').text.encode('utf-8')
    return( title + ':' + link)

#----------------------------------------------------------------
def url2file(url) :
    file=url
    #file=re.sub(':','_',url)
    file=re.sub('\/','@',file)
    return(file)


#----------------------------------------------------------------
def documentsInfo() :
  for i in range(0,len(urls)) :
    #print(str(i) + " - " + documentInfo(urls[i]) + ' ' + urls[i])
    print("{:3} {:<60.60} {}".format(str(i),documentInfo(urls[i]),urls[i]))

#----------------------------------------------------------------
def cached(file) :
    return("cache/" + file)
    

#----------------------------------------------------------------
def documentsCache() :
  for i in range(0,len(urls)) :
    file=urllib2.urlopen(urls[i])
    print("Caching file " + urls[i] + " " + str(i) + "/" + str(len(urls)))
    out=open(cached(url2file(urls[i])),'w')
    out.write(file.read())
    out.close()

#----------------------------------------------------------------
def rss(url,filter,prefix,download) :
  #tree = ET.ElementTree(file=urllib2.urlopen(url))
  tree = ET.ElementTree(file=open(cached(url2file(url))))
  root=tree.getroot()
  count=0
  print(documentInfo(url))
  for el in tree.iter(tag='item'):
    text=el.find('title').text.encode('utf-8')
    mp3=el.find('enclosure').attrib['url']
    if re.search(filter,text) is None :
      continue
    part=getNum(text)
    sPart=str(count)
    if part :
      sPart=part.group()
      sPart=re.sub('\(','',sPart)
      sPart=re.sub('\)','',sPart)
      sPart=re.sub('/','-',sPart)
    else :
      count += 1
    file=prefix + '_' + sPart + '.mp3'
    print '{:<100.100} wget -O {:s} {:s}'.format(text, file, mp3 )
    if download :
      cmd='/usr/bin/wget -O ' + file + ' ' + mp3
      print(cmd)
      os.system("nohup " + cmd + "&")

#----------------------------------------------------------------
def fList(args=None) :
  documentsInfo()

#----------------------------------------------------------------
def fCache(args=None) :
  documentsCache()
  
#----------------------------------------------------------------
def fScan(args) :
  url=urls[int(args.item)]
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

parserCache = subparsers.add_parser('cache', help='a help')
parserCache.set_defaults(func=fCache)

parserScan = subparsers.add_parser('scan', help='a help')
parserScan.set_defaults(func=fScan)
parserScan.add_argument('item',nargs='?',help="item to scan (given by list)")
parserScan.add_argument('--filter','-f',nargs=1,help="filter for scan")
parserScan.add_argument('--prefix','-p',nargs=1,help="prefix for filename")
parserScan.add_argument('--download',help="download",action="store_true")

args=parser.parse_args()
args.func(args)