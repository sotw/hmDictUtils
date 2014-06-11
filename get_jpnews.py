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
#from uniseg import Wrapper

global DB
global tTarget
global args
global ARGUDB
global _wrap
global LINKS

LINKS = []
ARGUDB = []
_wrap = TextWrapper()
_wrap.width = 34

#_wrap = Wrapper()
#_wrap.textextents =
#t_wrap.wrap_width


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

def aozoraFmtStr(rubyString):
	rubyString = rubyString.replace('<ruby>','') 
	rubyString = rubyString.replace('</ruby>','') 
	rubyString = rubyString.replace('<rb>','') 
	rubyString = rubyString.replace('</rb>','')
	rubyString = rubyString.replace('<rt>','\xe3\x80\x8a') 
	rubyString = rubyString.replace('</rt>','\xe3\x80\x8b') 
	return rubyString

def getReleaseNoteDetail(tDetail):
	#print tDetail
	#raw_input()
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

	#comments = tree.xpath('//comment()')
	#for c in comments:
	#	p = c.getparent()
	#	p.remove(c)

	etree.strip_tags(tree,'p')
	etree.strip_tags(tree,'i')
	etree.strip_tags(tree,'br')
	etree.strip_elements(tree, 'span', with_tail=False)
	etree.strip_tags(tree, 'a')
	etree.strip_tags(tree, 'b')
	etree.strip_tags(tree, 'i')
	etree.strip_tags(tree, 'h2')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')
	mTitle = ''
	#titles = tree.xpath("//h1")
	#for entry in titles:
	#	if entry.text is not None:
	#		mTitle = entry.text
	#		break
	#print paintRED(result,'<h1')
	#raw_input()

	titles = re.findall('<h1>(.+?)</h1>',result,re.DOTALL)
	#print titles
	#raw_input()
	for entry in titles:
		fmtString = aozoraFmtStr(entry.strip('\n'))
		mTitle = fmtString
		break

	#print paintRED(result,'class="nwbody')
	#raw_input()
	#resultSet = tree.xpath("//div[@class='nwbody']") #for original
	resultSet = re.findall('<div class="nwbody">(.+?)</div>',result,re.DOTALL) #for hiraganamegane

	#print resultSet
	#raw_input()

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
		fmtString = aozoraFmtStr(entry.strip('\n'))
		print '    '+fmtString
		thisScreen.append(fmtString)
		#if entry.text is not None:			
		#	for line in _wrap.wrap(entry.text):			
		#		line = dedent(line)
		#		print '    '+line
		#		thisScreen.append('    '+line)
		#break
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
	elif option == 'dropbox':
		bigChunkStr = ''
		for line in thisScreen:		
			if len(line) != 0 :
				bigChunkStr = bigChunkStr+re.sub(r'\[[0-9]+m','',line)+'\n'			
		home = expanduser('~')		
		jpFileTitle = re.sub(r'\xe3\x80\x8a.+?\xe3\x80\x8b','',mTitle)
		#jpFileTitle = re.sub(r'\xe3\x80\x8b','',jpFileTitle)		
		print home+'/Dropbox/JpRead/'+jpFileTitle+'.txt'
		f = open(home+'/Dropbox/JpRead/'+jpFileTitle+'.txt','w')
		bigChunkStr = re.sub(r'-+?\n','\n',bigChunkStr)
		bigChunkStr = re.sub(r'<div.+?</div>','',bigChunkStr)
		f.write(bigChunkStr)
		f.close




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
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='UTF-8')

	#print repr(result)
	#raw_input()
	#print paintRED(repr(result),'<div class="lst1t">')
	global LINKS
    #head line#
	headLines = re.findall('<h2 class="ch08">\n<a href="(.+?)" onclick="clickCount\(\'news_top.+?">(.+?)</a>.+?!--ch08_2-->\n<p>(.+?)<a',result,re.DOTALL)

	#print len(headLines)
	#print headLines

	#raw_input()
	#print clrTx('HEADLINES:','BLUE')
	ScreenI.append(clrTx('HEADLINES:','BLUE'))
	for headLine in headLines:
		#print headLine		
		#print clrTx(headLine[1],'YELLOW')		
		fmtString = aozoraFmtStr(headLine[1])
		ScreenI.append(clrTx(fmtString,'YELLOW'))
		fmtString = aozoraFmtStr(headLine[2])
		text = codecs.decode(fmtString,'utf-8')		
		#print text
		#print "==="
		for line in _wrap.wrap(text):
			#print '    '+line
			ScreenI.append('    '+line)
		LINKS.append(headLine[0])
		#print clrTx('Input:'+str(cnt)' for more','GREY30')
		ScreenI.append(clrTx('Input:'+str(len(LINKS)-1)+' for more','GREY30'))
		#print clrTx(headLine[0],'GREY30')

	majorLines = re.findall('<div class="lst1t">\n<ul>\n<li>\n<a href="(.+?)" onclick="clickCount\(\'news_top.+?">(.+?)</a>',result)
	#print len(majorLines)
	#raw_input()
	#print clrTx('MAJORLINES:','BLUE')
	ScreenI.append(clrTx('MAJORLINES:','BLUE'))
	cnt = 0
	for majorLine in majorLines:
		#print clrTx(majorLine[1],'YELLOW')		
		fmtString = aozoraFmtStr(majorLine[1])
		ScreenI.append(clrTx(fmtString,'YELLOW'))
		#LINKS.append('http://news.goo.ne.jp/'+majorLine[0])	#for original
		LINKS.append(majorLine[0])	#for hiraganamegane
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
		if (sn is not None) and (sn < len(LINKS) ):		
			getReleaseNoteDetail(LINKS[sn])
		else:
			print "Have a nice day"

	return

def setup_logging(level):
	global DB
	DB = logging.getLogger('get_jpnews') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args
	parser = argparse.ArgumentParser(description='A get_jpnews Reader') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/get_jpnews.db') #replace
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
