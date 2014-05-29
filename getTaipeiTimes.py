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

global DB
global tTarget
global args
global ARGUDB
global _wrap

ARGUDB = []
_wrap = TextWrapper()

def repeatStr(string_to_expand, length):
	return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def parseInt(sin):
	m = re.search(r'^(\d+)[.,]?\d*?',str(sin))
	return int(m.groups()[-1]) if m and not callable(sin) else None

def getReleaseNoteDetail(tDetail):
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
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	mTitle = ''
	titles = tree.xpath("//h1[@class='title']")
	for entry in titles:
		if entry.text is not None:
			mTitle = entry.text
			break

	resultSet = tree.xpath("//div[@class='text']")
	#print len(resultSet)

	os.system('clear')	
	print " "
	print '  '+clrTx(mTitle,'YELLOW')
	print repeatStr('-', 78)
	print ' '
	for entry in resultSet:
		if entry.text is not None:			
			for line in _wrap.wrap(entry.text):			
				line = dedent(line)
				print '    '+line
		break
	print ' '
	print repeatStr('-', 78)

'''For programming'''
def paintRED(string,target):
	string = string.replace(target,clrTx(target,'RED'))
	return string

def doStuff(tTarget):
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

	etree.strip_tags(tree,'span')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	#print result
	#print paintRED(result,'<li><h3>')

	os.system('clear')
	LINKS = []
    #head line#
	headLines = re.findall('<div class="ma">\r<h1><a href="([^"]+)">([^<]+)</a></h1>\r<h4>([^<]+)<',result)
	#print len(headLines)
	print clrTx('HEADLINES:','BLUE')
	for headLine in headLines:
		#print headLine		
		print clrTx(headLine[1],'YELLOW')		
		for line in _wrap.wrap(headLine[2]):
			print '    '+line
		LINKS.append('http://www.taipeitimes.com/'+headLine[0])
		print clrTx('Input:'+str((len(LINKS)-1))+' for more','GREY30')
		#print clrTx(headLine[0],'GREY30')

	#majorLines only 4 is for majorLines
	majorLines = re.findall('<h3><a href="([^"]+)">([^<]+)</a></h3>([^<]+)<',result)

	cnt = 0
	print clrTx('MAJORLINES:','BLUE')
	for majorLine in majorLines:
		if cnt == 4 :
			break
		print clrTx(majorLine[1],'YELLOW')		
		for line in _wrap.wrap(majorLine[2]):
			print '    '+line
		LINKS.append('http://www.taipeitimes.com/'+majorLine[0])
		print clrTx('Input:'+str((len(LINKS)-1))+' for more','GREY30')
		#print clrTx(majorLine[0],'GREY30')
		#print majorLine
		cnt+=1

	#print LINKS
	sn=None
	sn=raw_input('Which one you want to check?(Sn)>')
	sn = parseInt(sn)
	if sn is not None:		
		getReleaseNoteDetail(LINKS[sn])

	'''releaseNoteSet = re.findall('<div class="title"><a href="([^"]+)">([^<]+)</a>',result)
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
	return

def setup_logging(level):
	global DB
	DB = logging.getLogger('getTaipeiTimes')
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
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/getTaipeiTimes.db')
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
