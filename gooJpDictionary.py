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
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

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
   #etree.strip_tags(tree,'a')
   #etree.strip_tags(tree,'dt')
   #etree.strip_tags(tree,'dd')
   #etree.strip_tags(tree,'dl')
   
   result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='UTF-8')
   #DB(1, result)

   encoding = chardet.detect(result)
   #print encoding

   targetURL = ""
   lineSum = 0

   os.system('clear')

   resultSet = []

   #|class|howmany|
   arrangedSetA = []

   classSet = re.findall('class="allpage fs16">([^<]+)<',result)
   for className in classSet :
   	   if className is not None:   	   	   
   	   	   #print className
   	   	   arrangedSetA.append([className,0])

   howmanySet = re.findall('class="schnum">([^<]+)<',result)
   iCnt = 0
   for howmany in howmanySet :
   	   if howmany is not None:
   	   	   #print howmany
   	   	   numbers = re.findall('([0-9])',howmany)
   	   	   #for number in numbers:
   	   	   	   #print number
   	   	   arrangedSetA[iCnt][1] = numbers[1]
   	   iCnt += 1

   #print arrangedSetA

   #dtSet = tree.xpath("//dl[@class='allList']")
   #print len(dtSet)

   #|title|href|
   arrangedSetB = []

   aSet = tree.xpath("//dl[@class='allList']//dt/a")
   for e in aSet:
   	   if e.text is not None:
   	   	   arrangedSetB.append([e.text,e.get('href')])   	   	   
   	   	   DB(1, e.text+"|"+e.get('href'))


   #|explaination|
   arrangedSetC = []
   ddSet = tree.xpath("//dl[@class='allList']//dd")
   for e in ddSet:
   	   if e.text is not None:
   	   	   arrangedSetC.append(e.text)
   	   	   #print e.text+'\n'

   accumulation = 0
   for e in arrangedSetA:
		bSChineseWarning = False
		if e[0] == '\xe6\x97\xa5\xe4\xb8\xad\xe8\xbe\x9e\xe6\x9b\xb8' or e[0] == '\xe4\xb8\xad\xe6\x97\xa5\xe8\xbe\x9e\xe6\x9b\xb8':
			bSChineseWarning = True		
		print clrTx(e[0]+'\n','BLUE')
		for idx in range(int(e[1])):
			print clrTx(arrangedSetB[accumulation][0],'YELLOW')+clrTx(' > input('+str(accumulation)+')for more detail\n','GREY30')
			if bSChineseWarning == True:				
				print jianfan.jtof(arrangedSetC[accumulation])[0]
			else :
				print ripSentence(arrangedSetC[accumulation])
				#print tokenizedRomaji(ripSentence(arrangedSetC[accumulation]))
			accumulation+=1
		num = raw_input()
		iIn = parseInt(num)
		#[]==user can input detail url futher by any pause
		if iIn is not None:
			#print 'go %s'%(aSet[1].get('href'))			
			process = Popen(['python',INSFOLDER+'/gooDetailA.py','http://dictionary.goo.ne.jp'+aSet[iIn].get('href'),INSFOLDER,'1'])
			process.wait()
			break #for console user experience
					
   #myList = tree.xpath("//div[@class='allResultList']")
   #resultSet = handler(myList)
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
