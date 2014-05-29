#[]== Think this two-layered index seems common
#[]== 1. Index page 2. detail page
#[]== Rather than create two python, I should create one only

import os, sys, re, codecs
import argparse
import logging
import urllib, urllib2
#import textwrap
from os.path import expanduser
from subprocess import PIPE
from subprocess import Popen
from lxml import etree
from cStringIO import StringIO
from pprint import pprint
from HMTXCLR import clrTx
from textwrap import TextWrapper
from textwrap import dedent
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

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
	return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def parseInt(sin):
	m = re.search(r'^(\d+)[.,]?\d*?',str(sin))
	return int(m.groups()[-1]) if m and not callable(sin) else None

def getReleaseNoteDetail(tDetail):
	thisScreen = []
	opener = urllib2.build_opener()
	opener.addheader = [('User-Agent','Mozilla/5.0')]
	resp = opener.open(tDetail)
	if resp.code == 200:
		data = resp.read()
	elif resp.code == 404:
		print "Page do not exist"
		exit()
	else:
		print "Can not open page"
		exit()
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(data), parser)

	comments = tree.xpath('//comment()')
	for c in comments:
		p = c.getparent()
		if p is not None:
			p.remove(c)

	#etree.strip_tags(tree,'p')
	etree.strip_tags(tree,'br')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	mTitle = ''
	titles = tree.xpath("//header/h1")
	for entry in titles:
		if entry.text is not None:
			mTitle = entry.text
			print mTitle
			break

	resultSet = tree.xpath("//div[@id='lyrics-body-text']/p[@class='verse']")
	os.system('clear')	
	print " "
	thisScreen.append(" ")
	print '  '+clrTx(mTitle,'YELLOW')
	thisScreen.append('  '+clrTx(mTitle,'YELLOW'))
	print repeatStr('-', 78)
	thisScreen.append(repeatStr('-', 78))
	print ' '
	thisScreen.append(' ')
	for entry in resultSet:
		if entry.text is not None:			
			for line in _wrap.wrap(entry.text):			
				line = dedent(line)
				print '    '+line
				thisScreen.append('    '+line)

	print ' '
	thisScreen.append(' ')
	print repeatStr('-', 78)
	thisScreen.append(repeatStr('-', 78))
	option = raw_input()
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
		print home+'/.hmDict/simpleMail.py'
		if os.path.isfile(home+'/.hmDict/simpleMail.py') is True :

			process = Popen(prepareMailInfo(bigChunkStr))
			print "sending mail..."
			process.wait()			
			print "sent!"


'''For programming'''
def paintRED(string,target):
	string = string.replace(target,clrTx(target,'RED'))
	return string

def doStuff(tTarget):
	global preScreen
	opener = urllib2.build_opener()
	opener.addheader = [('User-Agent','Mozilla/5.0')]
	resp = opener.open(tTarget)
	if resp.code == 200 :
		data = resp.read()
		resp.close()
	elif resp.code == 404 :
		print "Page do not exist"
		exit()
	else:
		print "Can not open page"
		exit()

	parser = etree.HTMLParser(recover=True)
	tree = etree.parse(StringIO(data), parser)

	#etree.strip_tags(tree,'span')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	songSet = []
	#print result
	myList = tree.xpath("//table[@class='songs-table compact']/tbody/tr/td/a")
	#print myList
	for e in myList:
		#print e
	    if (e.get('href') is not None) and (e.text is not None):
	    	name = e.text.strip('\n')
	    	name = name.rstrip('Lyrics')
	    	songSet.append([name,e.get('href')])
	
	#print songSet
	screenShow = []
	cnt = 0
	for aSong in songSet:
		screenShow.append(str(cnt)+'|'+aSong[0])
		cnt+=1
	sn = ''
	while sn != None :
		os.system('clear')
		for line in screenShow:
			print line
		sn = parseInt(raw_input())
		if sn != None :
			getReleaseNoteDetail(songSet[sn][1])
	return

def setup_logging(level):
	global DB
	DB = logging.getLogger('get_lyrics')
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args
	parser = argparse.ArgumentParser(description='A Lyrics Search Utility Only By Artist Name')
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/get_lyrics.db')
	args = parser.parse_args()
	tTarget = 'http://www.metrolyrics.com/'+' '.join(args.query)+'-lyrics.html'
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
