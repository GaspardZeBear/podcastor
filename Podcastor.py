#!/usr/bin/python
import xml.etree.cElementTree as ET
import urllib.request
import re
import sys
import os
import argparse
import requests
import json
import logging

content=[]
            
#----------------------------------------------------------------
def getNum(text) :
  part=re.search('\(\d+/\d+\)',text)
  if part is None :
    part=re.search('\d+/\d+',text)
  return part

#----------------------------------------------------------------
def documentInfo(url) :
    try :
      tree = ET.ElementTree(file=open(cached(url2file(url)),'rb'))
    except :
      logging.warning(f'Error cache file {cached(url2file(url))}')
      raise
    root=tree.getroot()
    logging.debug(root)
    el=root.find('channel')
    title=el.find('title').text
    logging.debug(f'{title=}')
    link=el.find('link').text
    logging.debug(f'{link=}')
    return(title.lstrip() + ':' + link)

#----------------------------------------------------------------
def url2file(url) :
    file=url
    file=re.sub('\/','@',file)
    return(file)

#----------------------------------------------------------------
def documentsInfo(filter,args) :
  logging.debug("documentsInfo(filter,args)")
  for i in range(0,len(urls)) :
    logging.debug(f'{i=} {urls[i]=}')
    try :
      text=documentInfo(urls[i][1])
      if re.search(filter,text) is None :
        continue
      if args.url :
        print("{:3} {:<20.20} {:<80.80} {}".format( str(i), urls[i][0], documentInfo(urls[i][1]), urls[i][1]))
      else :
        print("{:3} {:<20.20} {}".format( str(i), urls[i][0], documentInfo(urls[i][1]).strip() ))
    except :
      logging.warning(f'Error cache file {urls[i]=}')

#----------------------------------------------------------------
def cached(file) :
    logging.debug("cache/" + file)
    return("cache/" + file)
    
#----------------------------------------------------------------
def documentCache(url) :
  print("Loading file " + url)
  try :
    r=requests.get(url)
    print("Caching file " + url)
    with open(cached(url2file(url)),'wb') as out : 
      out.write(r.content)
  except :
    logging.warning("Error")

#----------------------------------------------------------------
def documentsCache() :
  for i in range(0,len(urls)) :
    print("Prepare caching file " + urls[i][1] + " " + str(i+1) + "/" + str(len(urls)))
    documentCache(urls[i][1])

#----------------------------------------------------------------
def rss(url,urllen,txtlen,filter,prefix,download) :
  tree = ET.ElementTree(file=open(cached(url2file(url))))
  root=tree.getroot()
  count=0
  for el in tree.iter(tag='item') :
    text=el.find('title').text
    if re.search(filter,text) is None :
      continue
    count += 1
  print(documentInfo(url))
  for el in tree.iter(tag='item') :
    text=el.find('title').text
    pubDate=el.find('pubDate').text
    mp3=el.find('enclosure').attrib['url']
    if re.search(filter,text) is None :
      continue
    part=getNum(text)
    sPart='{:02d}'.format(count)
    if part :
      sPart=part.group()
      sPart=re.sub('\(','',sPart)
      sPart=re.sub('\)','',sPart)
      sPart=re.sub('/','-',sPart)
    else :
      count -= 1
    file=prefix + '_' + sPart + '.mp3'
    textNorm=text.encode('ascii',errors='replace')[0:txtlen]
    len=f'_<{txtlen}.{txtlen}'
    content.append(f'{pubDate:<16.16} {textNorm.decode("utf-8"):{len}} {mp3[0:urllen]}')

    if download :
      cmd='/usr/bin/wget --no-check-certificate -O ' + file + ' ' + mp3
      print(cmd)
      os.system("nohup " + cmd + "> /dev/null 2>&1 &")
  for item in reversed(content) :
    print(item)

#----------------------------------------------------------------
def fList(args=None) :
  logging.warning("flist")
  filter='.*'
  if args.filter :
    filter=args.filter[0]
  documentsInfo(filter,args)

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
  rss(url,int(args.urllen),int(args.txtlen),filter,prefix,args.download) 
  
#----------------------------------------------------------------

with open('URLS.json') as f :
  datas=json.load(f)
urls=[]
for url in datas["urls"] :
  if not url[0].startswith("#") :
    urls.append(url)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')
parser.add_argument('-v', '--verbose',
                    action='count',
                    dest='verbose',
                    default=0,
                    help="verbose output (repeat for increased verbosity)")

parserList = subparsers.add_parser('list', help='a help')
parserList.set_defaults(func=fList)
parserList.add_argument('--filter','-f',nargs=1,help="filter for scan")
parserList.add_argument('--url','-u',help="show url",default=False,action="store_true")


parserCache = subparsers.add_parser('cache', help='a help')
parserCache.set_defaults(func=fCache)
parserCache.add_argument('num',nargs='?',help="num of file to cache")

parserScan = subparsers.add_parser('scan', help='a help')
parserScan.set_defaults(func=fScan)
parserScan.add_argument('item',nargs='?',help="item to scan (given by list)")
parserScan.add_argument('--filter','-f',nargs=1,help="filter for scan")
parserScan.add_argument('--prefix','-p',nargs=1,help="prefix for filename")
parserScan.add_argument('--txtlen','-t',default="120",help="txt len on display")
parserScan.add_argument('--urllen','-l',default="30",help="url len on display")
parserScan.add_argument('--download','-d',help="download",action="store_true")
parserScan.add_argument('--url','-u',help="show url",default=False,action="store_true")
args=parser.parse_args()

loglevels=[logging.ERROR,logging.WARNING,logging.INFO,logging.DEBUG,1]
loglevel=loglevels[args.verbose] if args.verbose < len(loglevels) else loglevels[len(loglevels) - 1]
logging.basicConfig(stream=sys.stdout,format="%(asctime)s %(module)s %(name)s  %(funcName)s %(lineno)s %(levelname)s %(message)s", level=loglevel)

args.func(args)
