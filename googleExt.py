# Author Pei-Chen Tsai aka Hammer
# Ok, the line break position is impossible to 100% accurate currently, so just tune global parameter for your own purpose

from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib2
import sys
import os
import re
import codecs
from HMTXCLR import clrTx
from os.path import expanduser

global DB_FLT, DB_NOR, DB_ARG, DB_VER #verbose print
global TYPE_P, TYPE_H, TYPE_LI
global BREAK_CNT_P, BREAK_CNT_H, BREAK_CNT_LI
global ARGUDB #arugment database
global ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI
global tPage
global INSFOLDER

DB_FLT, DB_NOR, DB_ARG, DB_VER    = range(4)
TYPE_P, TYPE_H, TYPE_LI, TYPE_PRE = range(4)
BREAK_CNT_P   = 124
BREAK_CNT_H   = 96
BREAK_CNT_LI  = 120
ARGUDB        = []
ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI = range(4)
tPage         = ''
INSFOLDER = ''

def DB(level,msg):
   if int(level) == int(DB_FLT) :
      print msg

def contentStrip(iList):
	DB(1,'Doing stripping...')
	stack = []
	for e in iList:
		if e.text is not None:            
			stack.append(e.text)					
	return stack

def handler(iList):      
	DB(1,'ENTER p handler')
	ret = []
	DB(1, 'There are '+str(len(iList))+' interesting stuff found')
	if len(iList) > 0 :
		ret = contentStrip(iList)
	DB(1, 'LEAVE p handler')
	return ret

def htmlParser(tPage):
	opener = urllib2.build_opener()
	opener.addheaders = [#('Accept-Encoding','gzip,deflate,sdch'),
                         ('User-Agent','Mozilla/5.0')] #(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114')]
	resp = opener.open(tPage)
	#resp = urllib2.urlopen(tPage)
	if resp.code == 200 :
		data = resp.read()
		resp.close()
	elif resp.code == 404 :
		print "page do not exist"
		exit()
	else :
		print "can not open page"
		exit()
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(data), parser)
	#etree.strip_tags(tree,'em')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html",encoding='utf-8')
	#print result
	#DB(1, result)

	targetURL = ""
	lineSum = 0
	resultSet = re.findall('<h3 class="r"><a href="[^"]+">',result)#tree.xpath("//div[@class='rc']")
	print len(resultSet)
	for e in resultSet :
		if e is not None:			
			print e
	return resultSet


def prettyPrint(resultSet):
	passIstring = ''

	for result in resultSet:
		result = result.replace('breakHere','\n')
		result = result.replace('titleBreak','\n')
		#result = result.replace('idiom','\n\ridiom')
		#print len(result)
		for tag in ARGUDB:			
			result = result.replace(tag,clrTx('\n'+tag,'YELLOW'))
		if len(result) > 1 :
			passIstring = passIstring+result

	passIIStrSet = passIstring.split('\n')
	pauseCnt=0
	for strII in passIIStrSet:		
		bFound = False
		for tag in ARGUDB:
			try :
				strII.index(tag)
				bFound = True
				break
			except ValueError:
				bFound = False
		if bFound == False:
			strII = "    "+strII
		if pauseCnt <= 20 :
			print strII
			pauseCnt+=1
		else :			
			raw_input()
			print strII
			pauseCnt=0

def assignPageAndOverrideArgu():
   DB(DB_ARG,'ENTER overrideArgu')
   global tPage
   tPage = sys.argv[1]
   #print "tPage:"+tPage
   DB(DB_ARG,'LEAVE overrideArgu')

def loadArgumentDb():
	if os.path.isfile(INSFOLDER+'/argumentDbA') is True:
		f = codecs.open(INSFOLDER+'/argumentDbA',encoding='UTF-8',mode='r')
		if f is not None:
			for line in f:
				if line != '\n' and line[0] != '#':
					line = line.rstrip('\n')
					global ARGUDB
					ARGUDB.append(line)
			f.close()
		else:			
			DB(1, 'db file open fail')
	else :
		print 'argumentDbA doesn\'t existed'

def main():
   resultSet = htmlParser(tPage)
   #prettyPrint(resultSet)

def verify():
	if len(sys.argv) < 3 or len(sys.argv) > 4 :
		print "python pyYahooDictionary.py <tPage> <install path> <DB>"
		print "please use edict(bash scirpt) instead of using this"
		print "--"
		print "DB flag is option"
		exit()
	if len(sys.argv) == 4 :
		global DB_FLT
		global INSFOLDER
		INSFOLDER = sys.argv[2]
		DB_FLT = int(sys.argv[3])

if __name__ == '__main__':
   verify()
   loadArgumentDb()
   assignPageAndOverrideArgu()
   main()
