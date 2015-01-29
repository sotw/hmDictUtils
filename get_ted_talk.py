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


	#etree.strip_tags(tree,'p')
	#etree.strip_tags(tree,'i')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	mTitle = ''
	titles = tree.xpath("//h4[@class='h9 m5']/a")
	for entry in titles:
		if entry.text is not None:
			mTitle = entry.text
			break

	resultSet = tree.xpath("//span[@class='talk-transcript__fragment']")
	os.system('clear')
	thisScreen.append(" ")
	thisScreen.append('  '+clrTx(mTitle,'YELLOW'))
	thisScreen.append(repeatStr('-',78))
	thisScreen.append(' ')
	for result in resultSet:
		if result.text is not None:
			for text in _wrap.wrap(result.text):
				thisScreen.append('    '+text)
	thisScreen.append(' ')
	thisScreen.append(repeatStr('-',78))
	option = ''
	bSlowShow = False
	bLineBreakAt = 25
	while option == '' or option == 'slowShow' or option == 'showAll' :
		cnt = 0
		for line in thisScreen:
			print line
			if bSlowShow :
				if cnt >= bLineBreakAt :
					cnt = 0
					raw_input()
			cnt+=1
		print '<b>: back to index | <en>: English | <tw>: Traditional-Chinese'
		print '<slowShow>: pauseAtCertainLines | <showAll>: show all at once'
		print '<mail>: mail to myself (funciton not public!)'
		option = raw_input()
		if option == 'slowShow':
			bSlowShow = True
			bLinkBreakAt = parseInt(raw_input('please input pause at each ? lines'))
			os.system('clear')
		elif option == 'showAll':
			bSlowShow = False
		#print repr(option)

	if option == 'en' :
		tDetail = tDetail.split('?')[0]+'?language=en'
		getReleaseNoteDetail(tDetail)
	elif option == 'tw' :
		tDetail = tDetail.split('?')[0]+'?language=zh-tw'
		getReleaseNoteDetail(tDetail)
	elif option == 'mail':
		sendMail(thisScreen)

def sendMail(screen):
	bigChunkStr = ''
	mailLineCnt = 0
	for line in screen:
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
	else :
		print 'You don\'t have email plugin!, abort!!'
	raw_input()


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

	majorLines = re.findall('<h4 class="h9 m5">\n<a href="(.+?)".+?>(.+?)</a>',result,re.DOTALL)
	#print len(majorLines)
	#raw_input()
	ScreenI.append(clrTx('SPEECH:','BLUE'))
	cnt = 0
	for majorLine in majorLines:
		#print clrTx(majorLine[1],'YELLOW')
		ScreenI.append(clrTx(majorLine[1].strip('\n'),'YELLOW'))
		LINKS.append('http://www.ted.com'+majorLine[0].split('?')[0]+'/transcript')
		#print clrTx('Input:'+str((len(LINKS)-1))+' for more','GREY30')
		ScreenI.append(clrTx('Input:'+str((len(LINKS)-1))+' for more','GREY30'))
		#print clrTx(majorLine[0],'GREY30')
		#print majorLine
		cnt+=1

	#print LINKS
	sn=''
	while sn is not None :
		os.system('clear')
		#print ScreenI
		for item in ScreenI:
			print item
		sn=raw_input('Sn|tw|en|q >')
		#print repr(sn)
		ohInt = sn
		ohInt = parseInt(ohInt)
		if (ohInt is not None) and (ohInt < len(LINKS)):
			getReleaseNoteDetail(LINKS[ohInt])
		else:
			if sn == 'tw' :
				LINKS = []
				doStuff(tTarget+'&language=zh-tw')
			elif sn == 'en':
				LINKS = []
				doStuff(tTarget+'&language=en')
			else:
				print "Have a nice day"
				break
	return

def setup_logging(level):
	global DB
	DB = logging.getLogger('get_ted_talk_science') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args
	parser = argparse.ArgumentParser(description='A get_ted_talk_science Utility') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/get_ted_talk_science.db') #replace
	args = parser.parse_args()
	tTarget = ' '.join(args.query)
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
