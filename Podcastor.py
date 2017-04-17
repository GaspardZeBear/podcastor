#!/usr/bin/python

import xml.etree.cElementTree as ET
import urllib2
import re
import sys
import os

url='http://radiofrance-podcast.net/podcast09/rss_15537.xml'
url='http://radiofrance-podcast.net/podcast09/rss_10351.xml'
url='http://radiofrance-podcast.net/podcast09/rss_14486.xml'
url='http://radiofrance-podcast.net/podcast09/rss_11495.xml'
url='http://cdn1-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/qui-vive.xml'
url='http://radiofrance-podcast.net/podcast09/rss_14007.xml'
url='http://radiofrance-podcast.net/podcast09/rss_11475.xml'
url='http://radiofrance-podcast.net/podcast09/rss_10467.xml'
url='http://radiofrance-podcast.net/podcast09/rss_16274.xml'
url='http://radiofrance-podcast.net/podcast09/rss_11921.xml'
url='http://www.rtl.fr/podcast/100-live.xml'

def getNum(text) :
  part=re.search('\(\d+/\d+\)',text)
  if part is None :
    part=re.search('\d+/\d+',text)
  #print part
  return part
  
  

prefix='podcast'
filter='.*'
if len(sys.argv) > 1 and sys.argv[1] is not None :
  filter=sys.argv[1]
  if '=' in sys.argv[1] :
    filter,prefix=sys.argv[1].split('=')
  
download=False
if len(sys.argv) > 2 and sys.argv[2] is not None :
  if sys.argv[2] == 'download':
    download=True


tree = ET.ElementTree(file=urllib2.urlopen(url))

root=tree.getroot()
count=0
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
  print '{:120.120} wget -O {:s} {:s}'.format(text, file, mp3 )
  if download :
    cmd='/usr/bin/wget -O ' + file + ' ' + mp3
    print(cmd)
    os.system(cmd)

#wget -O candre-5-5.mp3 http://rf.proxycast.org/1285229558848561153/10351-07.04.2017-ITEMA_21284754-0.mp3  
