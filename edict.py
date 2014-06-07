# Author Pei-Chen Tsai aka Hammer
# Ok, the line break position is impossible to 100% accurate currently, so just tune global parameter for your own purpose

import os, sys, re, codecs
import urllib, urllib2
import argparse
import logging
import platform
from HMTXCLR import clrTx
from os.path import expanduser
from cStringIO import StringIO
from lxml import etree
from pprint import pprint

global DB
global args
global ARGUDB #arugment database
global tPage
global mProun

mProun = []
ARGUDB        = []
tPage         = ''
INSFOLDER = ''
bWindows = False

if 'Windows' in platform.platform():
	bWindows = True

def cp65001(name):
    if name.lower()=='cp65001':
	return codecs.lookup('utf-8')

#def cp950(name):
#    if name.lower()=='cp950':
#	return codecs.loopup('utf-8')

codecs.register(cp65001)
#codecs.register(cp950)

def repeatStr(string_to_expand, length):
	return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def htmlParser(tPage):
	resp = urllib2.urlopen(tPage)
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
	#etree.strip_tags(tree,'strong')
	etree.strip_tags(tree,'samp')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding="utf-8")
	
	#print repr(result)
	global mProun
	mProun = re.findall('<span class="proun_type">(.+?)</span><span class="proun_value">(.+?)</span>',result)

	#print len(mProun)
	#raw_input()
	mTitle = re.findall('<span class="yschttl">(.+?)</span>',result)

	etree.strip_tags(tree,'span')
	etree.strip_tags(tree,'a')

	
	for p in tree.xpath("//p"):
  	  p.tail = 'breakHere' + p.tail if p.tail else 'breakHere'
	etree.strip_tags(tree,'p')
	etree.strip_tags(tree,'b')
	for h5 in tree.xpath("//h5"):
   	   h5.tail = 'titleBreak' + h5.tail if h5.tail else 'titleBreak'
	etree.strip_tags(tree,'h5')
	etree.strip_tags(tree,'ol')
	etree.strip_tags(tree,'li')
	etree.strip_tags(tree,'code')

	#result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
	#DB(1, result)

	resultSet = []
	targetURL = ""
	lineSum = 0
	myList = tree.xpath("//ul[@class='explanation_wrapper']")
	for e in myList:
		if e.text is not None:
			resultSet.append(e.text)

	for tTitle in mTitle:
		resultSet.insert(0,clrTx(tTitle,'AUQA')+'\n')

	guessList = tree.xpath("//h2/i")
	if len(guessList) != 0 :
   	   for e in guessList :
   	   	   if e.text is not None:
   	   	   	   resultSet.append('\n You mean:'+e.text+' ?')
   	   	   	   #print '\n You mean:'+e.text+' ?'

	return resultSet

#[]== maybe textwrapper, it's better than this hardcode 
def prettyPrint(resultSet):	
	if bWindows :
		os.system('cls')
	else:
		os.system('clear')
	
	passIstring = ''

	print " "
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
	#print passIIStrSet
	totalCnt=0
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
		if bFound == False and totalCnt != 0:
			strII = "    "+strII

		if pauseCnt <= 20 :
			pauseCnt+=1
		else :			
			raw_input()
			pauseCnt=0

		if totalCnt == 0 :
			print repeatStr("-",len(strII))
		try:		    
			if bWindows :
				print strII+'\n'
			else:
				print strII
		except IOError:
		        #do nothing, why windows raise IOError everything-.-?
			a = 1

		if totalCnt == 0 :
			print repeatStr("-",len(strII))

		if totalCnt == 0:
			for proun in mProun:			    
				print '    '+proun[0]+' '+proun[1]				
		totalCnt+=1

def loadArgumentDb():
	home = expanduser('~')
	if os.path.isfile(home+args.database) is True:
		f = codecs.open(home+args.database,encoding='UTF-8',mode='r')
		if f is not None:
			for line in f:
				if line != '\n' and line[0] != '#':
					line = line.rstrip('\n')
					global ARGUDB					
					ARGUDB.append(line)
			f.close()
		else:			
			DB.error('db file open fail')
	else :
		print 'database doesn\'t existed'
	#print ARGUDB
	#raw_input()

def main():
   resultSet = htmlParser(tPage)
   prettyPrint(resultSet)

def setup_logging(level):
	global DB
	DB = logging.getLogger('get_ted_talk_science') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tPage
	global args
	parser = argparse.ArgumentParser(description='A English Dictionary Utility') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/edict.db') #replace
	args = parser.parse_args()
	tPage = ' '.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	if not tPage:
		parser.print_help()

if __name__ == '__main__':
	verify()
	loadArgumentDb()
	main()
