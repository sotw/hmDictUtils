#[]== Think this two-layered index seems common
#[]== 1. Index page 2. detail page
#[]== Rather than create two python, I should create one only

import os, sys, re, codecs
import argparse
import logging
import urllib
from urllib import request, error
import requests
#import textwrap
from os.path import expanduser
from subprocess import PIPE
from subprocess import Popen
from lxml import etree
from io import StringIO 
from pprint import pprint
from HMTXCLR import clrTx
from textwrap import TextWrapper
from textwrap import dedent
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from subprocess import check_output
from bs4 import BeautifulSoup, NavigableString
import time

global DB
global tTarget
global args
global ARGUDB
global _wrap
global LINKS
global preScreen

preScreen = []
LINKS = []
ARGUDB = []
DOWNLOAD_LINKS = []
_wrap = TextWrapper()

def prepareMailInfo(mailMsg):
	home = expanduser('~')
	iOut = []
	iOut.append('python')
	iOut.append(home+'/.hmDict/simpleMail.py')
	iOut.append(mailMsg)
	return iOut

def repeatStr(string_to_expand, length):
	return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

def parseInt(sin):
	m = re.search(r'^(\d+)[.,]?\d*?',str(sin))
	return int(m.groups()[-1]) if m and not callable(sin) else None

def getDetail(tDetail):
    thisScreen = []
    #resp = urllib.request.urlopen(url=tDetail)
    resp = requests.get(tDetail)
    data = resp.text
    soup = BeautifulSoup(data, features="lxml")
    print("beautifulSoup result 2")
    photo = soup.find('div',{'class':'photo'})
    print(photo)
    for child in photo.children:
        #print(child.name)
        if child.name == 'a':
            for mago in child.children:
                #print(mago.name)
                if mago.name == 'img':
                    DOWNLOAD_LINKS.append(mago['src'])

def getImgs():
    cnt = 0
    for link in DOWNLOAD_LINKS:
        print(str(cnt)+":"+link)
        out = check_output(["wget", link, "-O",str(cnt)+".jpg"])
        time.sleep(5)
        cnt+=1

'''For programming'''
def paintRED(string,target):
	string = string.replace(target,clrTx(target,'RED'))
	return string

def doStuff(tTarget):
    global preScreen
    global LINKS
    print(tTarget)
    #resp = urllib.request.urlopen(url=tTarget)
    resp = requests.get(tTarget)
    data = resp.text
    soup = BeautifulSoup(data,features="lxml")
    print("beautifulSoup result")
    bigIndex = soup.find('div',{'class':'gallery'})
#    result += soup.findAll('li',{'class':['lh-22 mh-22 ml-50 mt-12 mb-12','lh-22 mh-22 ml-50 mt-12 mb-12 last']});
    cnt = 0
    print(bigIndex)
    print(type(bigIndex))
    #for link in bigIndex['a']:
    #    print(link)
    print(bigIndex.name)
 #   print(bigIndex['a'])

    print("=======")
    for child in bigIndex.children:
        #print(child)
        #print("555555555555555")
        #print(type(child))
        #print(child.name)
        if child.name == 'a':
            #print(len(child['href']))
            if len(child['href']) > 10:
                LINKS.append(child['href'])

    for link in LINKS:
        #print(link)
        getDetail(link)

    #aIndex = BeautifulSoup(bigIndex.conetents,features="lxml")
    #for lv1 in bigIndex.children:
        #print(type(lv1.string))
     #   if isinstance(lv1.string, NavigableString):
     #       print(str(lv1.string))
            #print(lv1)
        #print(lv1)

        #my_a = BeautifulSoup(lv1, features="lxml")
        #if my_a.a != None:
        #    print(my_a.a['href'])
    #for headLine in headLines:

        #preScreen.append(str(cnt)+':'+clrTx(headLine.get_text(),'YELLOW'))
        #cnt+=1
        #pp = headLine.parent.parent
        #print(pp)
        #print("*****************")
        #print(pp['href'])
        #LINKS.append(pp['href'])
#    for item in LINKS:
#        print(item)
#        print("================")

    #sn=''
    #while sn is not None :
        #os.system('clear')
    #    for item in preScreen:
    #        print(item)
    #    sn=input('Which one you want to check?(Sn)>')
    #		#print repr(sn)
    #    sn = parseInt(sn)
    #    if (sn is not None) and sn < len(LINKS):
    #        #print(LINKS[sn])
    #        getDetail(LINKS[sn])
    #    else:
    #        print("Have a nice day")

	#print paintRED(result,'<li><h3>')
def setup_logging(level):
	global DB
	DB = logging.getLogger('get_taipei_times')
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args
	parser = argparse.ArgumentParser(description='A Taipei Times Reader')
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/get_taipei_times.db')
	args = parser.parse_args()
	tTarget = ' '.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	if not tTarget:
		parser.print_help()
		exit()
	setup_logging(log_level)

def loadDb():
	home = expanduser('~')
	if os.path.isfile(home+args.database) is True:
		f = open(home+args.database,'r')
		if f is not None:
			for line in f :
				if line != '\n' and line[0] != '#':
					line = line.rstrip('\n')
					global ARGUDB
					ARGUDB.append(line)
		f.close()
	else:
		DB.debug('override file is not exist')

def main():
    doStuff(tTarget)
    getImgs()

if __name__ == '__main__':
	verify()
	loadDb()
	main()
