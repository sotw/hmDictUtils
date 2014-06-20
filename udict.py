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
	opener = urllib2.build_opener()
	opener.addheader = [('User-Agent','Mozilla/5.0')]
	resp = opener.open(tTarget)
	if resp.code == 200 :
		data = resp.read()
		resp.close()
	elif resp.code == 404 :
		print "Page do not exist"
		exit()
	elif resp.code == 400:
		print "request error"
		exit()
	else:
		print "Can not open page"
		exit()

	parser = etree.HTMLParser(recover=True)
	tree = etree.parse(StringIO(data), parser)

	etree.strip_tags(tree,'span')
	etree.strip_tags(tree,'a')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')
	result = result.replace('<br>','\n')

	#print result
	#raw_input()
	#print paintRED(result,'<div class="me')
	#raw_input()
	global LINKS
    #head line#
	headLines = re.findall('<div class="meaning">(.+?)</div>[^<]+?<div class="example">(.+?)</div>',result,re.DOTALL)
	#print len(headLines)
	#print clrTx('HEADLINES:','BLUE')
	for headLine in headLines:		
		ScreenI.append(clrTx('meanings:','YELLOW'))
		for line in _wrap.wrap(headLine[0]):
			ScreenI.append('    '+line)
		ScreenI.append(clrTx('example:','YELLOW'))
		for line in _wrap.wrap(headLine[1]):
			ScreenI.append('    '+line)		
		ScreenI.append(repeatStr('-', 34))

	for item in ScreenI:
		if item == repeatStr('-', 34):
			raw_input()
		print item

	return

def setup_logging(level):
	global DB
	DB = logging.getLogger('udict') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args
	parser = argparse.ArgumentParser(description='A udict Utility') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/udict.db') #replace
	parser.add_argument('-t', '--target', dest='page', action='store', default='http://www.urbandictionary.com/define.php?term=')
	args = parser.parse_args()
	tTarget = args.page+'+'.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	if not tTarget:
		parser.print_help()
		exit()
	#elif args.read and args.kill:
	#	print "Flag conflict, some flag are exclusive"
	#	parser.print_help()
	#	exit()

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
	#print tTarget
	#raw_input()
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
