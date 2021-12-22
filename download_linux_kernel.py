#[]== Think this two-layered index seems common
#[]== 1. Index page 2. detail page
#[]== Rather than create two python, I should create one only

import os, sys, re, codecs
import argparse
import logging
import urllib, urllib2
import requests
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
global ctl

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
	resp = requests.get(tTarget)
	data = resp.text
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(data), parser)

	comments = tree.xpath('//comment()')
	for c in comments:
		p = c.getparent()
		p.remove(c)

	etree.strip_tags(tree,'p')
	etree.strip_tags(tree,'i')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	#mTitle = ''
	#titles = tree.xpath("//h1[@class='title']")


'''For programming'''
def paintRED(string,target):
	string = string.replace(target,clrTx(target,'RED'))
	return string

def doStuff(tTarget):
	ScreenI = []
	resp = requests.get(tTarget)
	data = resp.text
	parser = etree.HTMLParser(recover=True)
	tree = etree.parse(StringIO(data), parser)

	etree.strip_tags(tree,'span')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	#print repr(result)
	#print paintRED(result,'<li><h3>')
	global LINKS
    #head line# |mainline|version|date|link|
    #            0        1       2    3
	headLines = re.findall('<tr align="left">.+?<td>(.+?)</td>.+?<td><strong>(.+?)</strong></td>.+?<td>(.+?)</td>.+?<a href="(.+?)"',result, re.DOTALL)
	#print len(headLines)
	#raw_input()
	#print clrTx('HEADLINES:','BLUE')
	ScreenI.append(clrTx('SN | TAG | VERSION | DATE','BLUE'))
	for headLine in headLines:
		ScreenI.append(clrTx(str(len(LINKS)),'BLUE')+'|'+clrTx(headLine[0],'YELLOW')+'|'+clrTx(headLine[1],'AUQA')+'|'+clrTx(headLine[2],'GREEN'))
		iLink = headLine[3].strip('\n')
		#print repr(iLink)
		LINKS.append('https://www.kernel.org/'+iLink)
	
	#raw_input()
	#print LINKS
	sn=''
	while sn is not None :
		os.system('clear')
		for item in ScreenI:
			print item
		sn=input('Which kernel version you want to download?(Sn)>')
		#print repr(sn)
		sn = parseInt(sn)
		if (sn is not None) and (sn < len(LINKS)):		
			process = Popen(['wget',LINKS[sn]])
			process.wait()
		else:
			print("Have a nice day")

	return

def setup_logging(level):
	global DB
	DB = logging.getLogger('download_linux_kernel') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args
	parser = argparse.ArgumentParser(description='A download_linux_kernel Utility') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/download_linux_kernel.db') #replace
	args = parser.parse_args()
	tTarget = ' '.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	if not tTarget:
		parser.print_help()
		exit()
		
	setup_logging(log_level)

def refreshDb():
	global ARGUDB
	ARGUDB = []
	home = expanduser('~')
	if os.path.isfile(home+args.database) is True:
		f = open(home+args.database,'r')
		if f is not None:
			for line in f :
				if line != '\n' and line[0] != '#':
					line = line.rstrip('\n')
					ARGUDB.append(line)
		f.close()
	else:
		DB.debug('override file is not exist')

def idxMsg(message):
	return str(len(ARGUDB))+':'+message

def	doDump():
	for entry in ARGUDB:
		print entry

def doWriteLn(msg):
	f = open(home+args.database,'a')
	if f is not None:
		f.write(idxMsg(msg))
	f.close()

def doKillALn(number):
	ARGUDB.pop(number)
	f = open(home+args.database,'w')
	for entry in ARGUDB:
		f.write(idxMsg(entry))
	f.close()

def main():
	doStuff(tTarget)
	#if args.read :
	#	doDump()
	#elif args.kill:
	#	doKillALn(parseInt(tTarget))
	#else:
	#	doWriteLn(tTarget)

if __name__ == '__main__':	
	verify()	
	refreshDb()
	main()
