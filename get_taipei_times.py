#[]== Think this two-layered index seems common
#[]== 1. Index page 2. detail page
#[]== Rather than create two python, I should create one only

import os, sys, re, codecs
import argparse
import logging
import urllib
from urllib import request, error
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
from bs4 import BeautifulSoup,NavigableString

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
    resp = urllib.request.urlopen(url=tDetail)
    if resp.code == 200:
        data = resp.read()
    elif resp.code == 404:
        print("Page do not exist")
        exit()
    else:
        print("Can not open page")
        exit()
    soup = BeautifulSoup(data,features="lxml")
    print("beautifulSoup result")
    archives = soup.find('h1')
    resultSet = soup.findAll('p')
#	print(data)
    mTitle = archives.get_text()
	#print len(resultSet)
    os.system('clear')
    print(" ")
    thisScreen.append(" ")
    print("  "+clrTx(mTitle,'YELLOW'))
    thisScreen.append('  '+clrTx(mTitle,'YELLOW'))
    print(repeatStr('-', 78))
    thisScreen.append(repeatStr('-', 78))
    print(" ")
    thisScreen.append(' ')
    for entry in resultSet:
        #print(entry.get_text())
        if entry.get_text() is not None:
            cnt = 0
            for line in _wrap.wrap(entry.get_text()):
                line = dedent(line)
                if cnt % 2 == 1:
                    print("    "+clrTx(line,'AUQA'))
                else:
                    print("    "+clrTx(line,'WHITE'))
                    thisScreen.append('    '+line)
                    cnt+=1
    print(" ")
    thisScreen.append(' ')
    print(repeatStr('-', 78))
    thisScreen.append(repeatStr('-', 78))
    option = input()
'''
    #hidden function for my own
    if option == 'm' :
		bigChunkStr = ''
		mailLineCnt = 0
		for line in thisScreen:
			if len(line) != 0 :
				if mailLineCnt == 1 :
					line = '####'+line #prepare to do markdown tranformation
				bigChunkStr = bigChunkStr+re.sub(r'\[[0-9]+m','',line)+'\n'
				mailLineCnt+=1
		home = expanduser('~')
		print(home+"/.hmDict/simpleMail.py")
		if os.path.isfile(home+'/.hmDict/simpleMail.py') is True :

			process = Popen(prepareMailInfo(bigChunkStr))
			print("sending mail...")
			process.wait()
			print("sent!")
'''

'''For programming'''
def paintRED(string,target):
	string = string.replace(target,clrTx(target,'RED'))
	return string

def doStuff(tTarget):
    global preScreen
    global LINKS
    resp = urllib.request.urlopen(url=tTarget)
    if resp.code == 200 :
        data = resp.read()
        resp.close()
    elif resp.code == 404 :
        print("Page do not exist")
        exit()
    else:
        print("Can not open page")
        exit()
    soup = BeautifulSoup(data,features="lxml")
    print("beautifulSoup result")
    headLines = soup.findAll('h1',{'class','bf2'})
#    result += soup.findAll('li',{'class':['lh-22 mh-22 ml-50 mt-12 mb-12','lh-22 mh-22 ml-50 mt-12 mb-12 last']});
    cnt = 0
    for headLine in headLines:
        preScreen.append(str(cnt)+':'+clrTx(headLine.get_text(),'YELLOW'))
        cnt+=1
        pp = headLine.parent.parent
        #print(pp)
        #print("*****************")
        #print(pp['href'])
        LINKS.append(pp['href'])
#    for item in LINKS:
#        print(item)
#        print("================")

    sn=''
    while sn is not None :
        #os.system('clear')
        for item in preScreen:
            print(item)
        sn=input('Which one you want to check?(Sn)>')
		#print repr(sn)
        sn = parseInt(sn)
        if (sn is not None) and sn < len(LINKS):
            #print(LINKS[sn])
            getDetail(LINKS[sn])
        else:
            print("Have a nice day")

	#print paintRED(result,'<li><h3>')
'''
	global LINKS
    #head line#
	headLines = re.findall('<div class="ma">\r<h1><a href="([^"]+)">([^<]+)</a></h1>\r<h4>([^<]+)<',result)
	#print len(headLines)
	#print clrTx('HEADLINES:','BLUE')
	preScreen.append(clrTx('HEADLINES:','BLUE'))
	for headLine in headLines:
		#print headLine
		#print clrTx(headLine[1],'YELLOW')
		preScreen.append(clrTx(headLine[1],'YELLOW'))
		for line in _wrap.wrap(headLine[2]):
			#print '    '+line
			preScreen.append('    '+line)
		LINKS.append('http://www.taipeitimes.com/'+headLine[0])
		#print clrTx('Input:'+str(cnt)' for more','GREY30')
		preScreen.append(clrTx('Input:'+str(len(LINKS)-1)+' for more','GREY30'))
		#print clrTx(headLine[0],'GREY30')

	#majorLines only 4 is for majorLines
	majorLines = re.findall('<h3><a href="([^"]+)">([^<]+)</a></h3>([^<]+)<',result)
	#print clrTx('MAJORLINES:','BLUE')
	preScreen.append(clrTx('MAJORLINES:','BLUE'))
	cnt = 0
	for majorLine in majorLines:
		if cnt == 4 :
			break
		#print clrTx(majorLine[1],'YELLOW')
		preScreen.append(clrTx(majorLine[1],'YELLOW'))
		for line in _wrap.wrap(majorLine[2]):
			#print '    '+line
			preScreen.append('    '+line)
		LINKS.append('http://www.taipeitimes.com/'+majorLine[0])
		#print clrTx('Input:'+str((len(LINKS)-1))+' for more','GREY30')
		preScreen.append(clrTx('Input:'+str((len(LINKS)-1))+' for more','GREY30'))
		#print clrTx(majorLine[0],'GREY30')
		#print majorLine
		cnt+=1

	#print LINKS
	sn=''
	while sn is not None :
		os.system('clear')
		for item in preScreen:
			print(item)
		sn=raw_input('Which one you want to check?(Sn)>')
		#print repr(sn)
		sn = parseInt(sn)
		if (sn is not None) and sn < len(LINKS):
			getReleaseNoteDetail(LINKS[sn])
		else:
			print("Have a nice day")
    releaseNoteSet = re.findall('<div class="title"><a href="([^"]+)">([^<]+)</a>',result)
	cnt = 0
	for e in releaseNoteSet:
		print "SN:%d|%s"%(cnt,e[1])
		cnt+=1
	sn=None
	sn=raw_input('Which one you want to check?(Sn)')
	sn = parseInt(sn)
	if sn is not None:
		getReleaseNoteDetail('http://www.pathofexile.com'+releaseNoteSet[sn][0])
	'''

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

if __name__ == '__main__':
	verify()
	loadDb()
	main()
