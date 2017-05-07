#!/usr/bin/python

import xml.etree.cElementTree as ET
import urllib2
import re
import sys
import os
import argparse

urls=list()
urls.append('http://radiofrance-podcast.net/podcast09/rss_15537.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_10351.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_14486.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_11495.xml')
urls.append('http://cdn1-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/qui-vive.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_14007.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_11475.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_10467.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_16274.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_11921.xml')
urls.append('http://www.rtl.fr/podcast/100-live.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_10192.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_10078.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_10177.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_12360.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_13937.xml')
urls.append('http://radiofrance-podcast.net/podcast09/rss_16173.xml')

url='http://radiofrance-podcast.net/podcast09/rss_10192.xml'
#----------------------------------------------------------------
def getNum(text) :
  part=re.search('\(\d+/\d+\)',text)
  if part is None :
    part=re.search('\d+/\d+',text)
  #print part
  return part

#----------------------------------------------------------------
def documentInfo(url) :
    tree = ET.ElementTree(file=urllib2.urlopen(url))
    root=tree.getroot()
    el=tree.iter(tag='channel').next()
    title=el.find('title').text.encode('utf-8')
    link=el.find('link').text.encode('utf-8')
    return( title + ':' + link)

#----------------------------------------------------------------
def documentsInfo() :
  for i in range(0,len(urls)) :
    #print(str(i) + " - " + documentInfo(urls[i]) + ' ' + urls[i])
    print("{:3} {:<60.60} {}".format(str(i),documentInfo(urls[i]),urls[i]))
    
#----------------------------------------------------------------
def rss(url,filter,prefix,download) :
  print 'rss : {} {} {} {}'.format(url,filter,prefix,download)
  tree = ET.ElementTree(file=urllib2.urlopen(url))
  root=tree.getroot()
  count=0
  print(documentInfo(url))
  for el in tree.iter(tag='item'):
    text=el.find('title').text.encode('utf-8')
    mp3=el.find('enclosure').attrib['url']
    if re.search(filter,text) is None :
      continue
    #part=re.search('\(\d+/\d+\)',text)
    part=getNum(text)
    sPart=str(count)
    if part :
      sPart=part.group()
      sPart=re.sub('\(','',sPart)
      sPart=re.sub('\)','',sPart)
      sPart=re.sub('/','-',sPart)
    else :
      count += 1
  #text=re.sub('^|!|:|\s+|,|\.|\(|\)|\'|\\\\|/','_',text)
  #text=re.sub('_{2,}','',text)
    file=prefix + '_' + sPart + '.mp3'
    print '{:<120.120} wget -O {:s} {:s}'.format(text, file, mp3 )
    if download :
      cmd='/usr/bin/wget -O ' + file + ' ' + mp3
      print(cmd)
      os.system(cmd)

#wget -O candre-5-5.mp3 http://rf.proxycast.org/1285229558848561153/10351-07.04.2017-ITEMA_21284754-0.mp3  
  
#----------------------------------------------------------------
prefix='podcast'
filter='.*'
parser = argparse.ArgumentParser()
parser.add_argument('action',nargs='?',default='list',help="action : list, scan")
parser.add_argument('item',nargs='?',help="item to scan (given by list)")
parser.add_argument('--filter',nargs=1,help="filter for scan")
parser.add_argument('--prefix',nargs=1,help="prefix for filename")
parser.add_argument('--download',help="download",action="store_true")
args=parser.parse_args()
print(args.action)

if args.action == 'list' :
  documentsInfo()
  sys.exit()
  
if args.action == 'scan' :
  url=urls[int(args.item)]
  filter='.*'
  if args.filter :
    filter=args.filter[0]
  prefix='podcast'
  if args.prefix :
    prefix=args.prefix[0]
  rss(url,filter,prefix,args.download)

    

