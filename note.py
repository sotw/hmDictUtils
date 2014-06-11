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
global storePath

LINKS = []
ARGUDB = []
_wrap = TextWrapper()
storePath = ''

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
	else:
		print "Can not open page"
		exit()

	parser = etree.HTMLParser(recover=True)
	tree = etree.parse(StringIO(data), parser)

	etree.strip_tags(tree,'span')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	#print result
	#print paintRED(result,'<li><h3>')
	global LINKS
    #head line#
	headLines = re.findall('<div class="ma">\r<h1><a href="([^"]+)">([^<]+)</a></h1>\r<h4>([^<]+)<',result)
	#print len(headLines)
	#print clrTx('HEADLINES:','BLUE')
	ScreenI.append(clrTx('HEADLINES:','BLUE'))
	for headLine in headLines:
		#print headLine		
		#print clrTx(headLine[1],'YELLOW')
		ScreenI.append(clrTx(headLine[1],'YELLOW'))
		for line in _wrap.wrap(headLine[2]):
			#print '    '+line
			ScreenI.append('    '+line)
		LINKS.append('http://www.taipeitimes.com/'+headLine[0])
		#print clrTx('Input:'+str(cnt)' for more','GREY30')
		ScreenI.append(clrTx('Input:'+str(len(LINKS)-1)+' for more','GREY30'))
		#print clrTx(headLine[0],'GREY30')

	#majorLines only 4 is for majorLines
	majorLines = re.findall('<h3><a href="([^"]+)">([^<]+)</a></h3>([^<]+)<',result)
	#print clrTx('MAJORLINES:','BLUE')
	ScreenI.append(clrTx('MAJORLINES:','BLUE'))
	cnt = 0
	for majorLine in majorLines:
		if cnt == 4 :
			break
		#print clrTx(majorLine[1],'YELLOW')		
		ScreenI.append(clrTx(majorLine[1],'YELLOW'))
		for line in _wrap.wrap(majorLine[2]):
			#print '    '+line
			ScreenI.append('    '+line)
		LINKS.append('http://www.taipeitimes.com/'+majorLine[0])
		#print clrTx('Input:'+str((len(LINKS)-1))+' for more','GREY30')
		ScreenI.append(clrTx('Input:'+str((len(LINKS)-1))+' for more','GREY30'))
		#print clrTx(majorLine[0],'GREY30')
		#print majorLine
		cnt+=1

	#print LINKS
	sn=''
	while sn is not None :
		os.system('clear')
		for item in ScreenI:
			print item
		sn=raw_input('Which one you want to check?(Sn)>')
		#print repr(sn)
		sn = parseInt(sn)
		if (sn is not None) and (sn < len(LINKS)):		
			getReleaseNoteDetail(LINKS[sn])
		else:
			print "Have a nice day"

	return

def setup_logging(level):
	global DB
	DB = logging.getLogger('note') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args
	global storePath
	parser = argparse.ArgumentParser(description='A note Utility') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('-r', '--read', dest='read', action = 'store_true', default=False, help='read note, exclusive')
	parser.add_argument('-k', '--kill', dest='kill', action = 'store', default=None, help='remove a line, please attach a number behind -k, exclusieve')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/note.db') #replace
	args = parser.parse_args()
	tTarget = ' '.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	if args.read and args.kill != None:
		print "Flag conflict, some flag are exclusive"
		parser.print_help()
		exit()
	
	#if not tTarget:
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
		DB.debug('db file is not exist, but it\'s ok.\nIt will exist after the first time you writedown something')

def	doDump():
	os.system('clear')
	cnt = 0	
	for entry in ARGUDB:
		if cnt % 2 == 0 :
			print clrTx(str(cnt)+":"+entry,'YELLOW')		
		else:
			print clrTx(str(cnt)+":"+entry,'AUQA')
		cnt+=1

def doWriteLn(msg):
	home = expanduser('~')
	f = open(home+args.database,'a')
	if f is not None:
		f.write(msg+'\n')
	f.close()

def doKillALn(number):
	home = expanduser('~')
	if number != None:
		ARGUDB.pop(number)
		f = open(home+args.database,'w')
		for entry in ARGUDB:
			f.write(entry+'\n')
		f.close()
	else:
		print "Please give a number behind -k!"

def main():
	#doStuff(tTarget)
	if args.read :
		doDump()
	elif args.kill:
		doKillALn(parseInt(args.kill))
	else:
		doWriteLn(tTarget)

if __name__ == '__main__':	
	verify()	
	refreshDb()
	main()
