# Author Pei-Chen Tsai aka Hammer
# Ok, the line break position is impossible to 100% accurate currently, so just tune global parameter for your own purpose

from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib2
import chardet
import sys
import os
import re
import codecs
import jianfan
#from jNlp.jConvert import tokenizedRomaji
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

def DB(level,msg):
   if int(level) == int(DB_FLT) :
      print msg

#parseInt refer
#https://gist.github.com/lsauer/6088767
#https://gist.github.com/douglasmiranda/2174255
def parseInt(sin):
	m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
	return int(m.groups()[-1]) if m and not callable(sin) else None

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
   opener.addheaders = [('User-agent','Mozilla/5.0')]
   resp = opener.open(tPage)
   if resp.code == 200 :
      data = resp.read()
      resp.close()
   elif resp.code == 404 :
      print "page do not exist"
      exit()
   elif resp.code == 403 :
   	  print "Forbidden!"
   	  exit()
   else :
      print "can not open page"
      exit()
   parser = etree.HTMLParser()
   tree = etree.parse(StringIO(data), parser)
   etree.strip_tags(tree,'a')
   etree.strip_tags(tree,'b')
   etree.strip_tags(tree,'span')   
   #etree.strip_tags(tree,'dt')
   #etree.strip_tags(tree,'dd')
   #etree.strip_tags(tree,'dl')
   
   result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='UTF-8')
   #DB(1, result)

   encoding = chardet.detect(result)
   #print encoding

   targetURL = ""
   lineSum = 0

   resultSet = []

   myList = tree.xpath("//div[@class='meaning']")
   for e in myList:
   	   if e.text is not None:
   	   	   print e.text
   return resultSet

def ripSentence(text):
	text = text.replace(u'\uff11',u'\n\uff11') #1
	text = text.replace(u'\uff12',u'\n\uff12') #2 etc
	text = text.replace(u'\uff13',u'\n\uff13')
	text = text.replace(u'\uff14',u'\n\uff14')
	text = text.replace(u'\uff15',u'\n\uff15')
	text = text.replace(u'\uff16',u'\n\uff16')
	text = text.replace(u'\uff17',u'\n\uff17')
	text = text.replace(u'\uff18',u'\n\uff18')
	text = text.replace(u'\uff19',u'\n\uff19')
	return text

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
		print strII

def assignPageAndOverrideArgu():
   DB(DB_ARG,'ENTER overrideArgu')
   global tPage
   tPage = sys.argv[1]
   #print "tPage:"+tPage
   DB(DB_ARG,'LEAVE overrideArgu')

def loadArgumentDb():
	if os.path.isfile(INSFOLDER+'/argumentDbB') is True:
		f = codecs.open(INSFOLDER+'/argumentDbB',encoding='UTF-8',mode='r')
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
		print 'argumentDbB doesn\'t existed'

def main():
   resultSet = htmlParser(tPage)
   prettyPrint(resultSet)

def verify():
   if len(sys.argv) < 3 or len(sys.argv) > 4 :
      print "python gooJpDictionary.py <tPage> <DB>"
      print "please use jdict(bash scirpt) instead of using this"
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
