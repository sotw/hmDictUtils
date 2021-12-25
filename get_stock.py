#[]== Think this two-layered index seems common
#[]== 1. Index page 2. detail page
#[]== Rather than create two python, I should create one only

import os, sys, re, codecs
import argparse
import logging
import urllib
import requests
#import textwrap
from os.path import expanduser
from subprocess import PIPE
from subprocess import Popen
from lxml import etree
from io import StringIO
from pprint import pprint
from decimal import *

from requests.models import stream_decode_response_unicode
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
global staticStr
global ScreenI

staticStr = 'https://tw.stock.yahoo.com/quote/'
LINKS = []
ARGUDB = []
ScreenI = []
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
	string = string.replace(target, clrTx(target,'RED'))
	return string

def doStuff(tTarget,num):
	global ScreenI
	updownSymbol = u'\u2197'
	nums = num.split(":")
	num = nums[0]
	my_price = nums[1]	
	resp = requests.get(tTarget+num)
	data = resp.text
	#
	# print(data)
	parser = etree.HTMLParser(recover=True)
	tree = etree.parse(StringIO(data), parser)
	#etree.strip_tags(tree,'span')
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	#print(repr(result))
	#print(paintRED(repr(result),'function(win)'))
    #print paintRED(result,'stkname')

	# current value
	#headLines = re.findall('<div class=".+?">(.+?)</div>',repr(result),re.DOTALL)
	#headLines = re.findall('<div class=".+?">(.+?)</div>',repr(result),re.DOTALL)
	titles = tree.xpath('//h1[@class="C($c-link-text) Fw(b) Fz(24px) Mend(8px)"]')
	contents = tree.xpath('//span[@class="Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"]')
	if len(contents) == 0:
		contents = tree.xpath('//span[@class="Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"]')
		updownSymbol = u'\u2198'
	if len(contents) == 0:
		contents = tree.xpath('//span[@class="Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)"]')
		updownSymbol = u'\u2192'
	
	price = 0
	mytitle = 'NA'
	for content in contents:
		if content.text is not None:
			#print(content.get("value"))
			#print(content.text)
			price = content.text
			break
			
	for title in titles:
		if title.text is not None:
			mytitle = title.text
			break
	
	diff = Decimal(price) - Decimal(my_price)
	target_price = Decimal(Decimal(my_price)*Decimal('1.3'))
	ai_comment = " No comment"
	if diff > 0:
		ai_comment = " Hold! you don't earn enough!"
	if Decimal(price) - target_price > 0 :
		ai_comment = " Sell, you earn enough"
	if diff < 0:
		ai_comment = " https://www.youtube.com/watch?v=M2qroMuIluI&ab_channel=MaestroZiikos"
	ScreenI.append([num, mytitle, my_price, price, updownSymbol, diff, target_price, ai_comment])
	#ScreenI.append(content.text)

	#tNames = re.findall('<input type="hidden" name="stkname" value="(.+?)">',repr(result),re.DOTALL)
    #print len(headLines)
    #raw_input()
	#print(headLines)
	#for headLine in headLines:
	
	#	ScreenI.append(headLine)
        #print clrTx(headLine[1],'YELLOW')
		#for tName in tNames:
		#	ScreenI.append(clrTx(num,'YELLOW')+'('+tName+'):'+headLine)
		#	break
	
 
def setup_logging(level):
	global DB
	DB = logging.getLogger('get_stock') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args

	parser = argparse.ArgumentParser(description='A get_stock Utility') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/get_stock.db') #replace
	parser.add_argument('-a', '--add', dest='add', action = 'store_true', default=False, help='add stock number and price you bought or intent to bought')
	parser.add_argument('-r', '--read', dest='read', action = 'store_true', default=False, help='dump current monitor list')
	parser.add_argument('-k', '--kill', dest='kill', action = 'store_true', default=False, help='remove a stock from monitor list')
	parser.add_argument('-l', '--list', dest='listme', action = 'store_true', default=False, help='show current price,etc')
	args = parser.parse_args()
	tTarget = ' '.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	#if not tTarget:
	#	parser.print_help()
	#	exit()
	if args.read and args.kill:
		print("Flag conflict, some flag are exclusive")
		parser.print_help()
		exit()
	if not args.read and not args.kill and not args.add and not args.listme:
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

def	doDump():
	for entry in ARGUDB:
		print(entry)

def doDumpEx():
	global ScreenI
	for entry in ARGUDB:
		doStuff(staticStr,entry)
	print("|"+clrTx("Serial","CYAN")+"|"+clrTx("    Name","CYAN")+"|"+clrTx("    Cost","CYAN")+"|"+clrTx(" Current","CYAN")+ \
		"|"+clrTx("   Trend","CYAN")+"|"+clrTx("    Diff","CYAN")+"|"+clrTx("  Target","CYAN")+"|"+clrTx(" AI COMMENT","CYAN"))
	
	for item in ScreenI:
		target_str = f"|{item[0]:>6}|{item[1]:>6}|{item[2]:>8}|{item[3]:>8}|{item[4]:>8}|{item[5]:>8}|{item[6]:>8}|{item[7]}" 
		if item[4] == u'\u2197':
			print(clrTx(target_str,"RED"))
		elif item[4] == u'\u2198':
			print(clrTx(target_str,"GREEN"))
		elif item[4] == u'\u2192':
			print(clrTx(target_str,"WHITE"))

def doWriteLn(msg):
	msgs = msg.split(":")
	if(len(msgs) !=2):
		print(clrTx("you need to input get_stock -a [stock_num]:[my_base_price]",'YELLOW'))
	home = expanduser('~')
	f = open(home+args.database,'a')
	hit_flag = 0
	hit_index = 0
	for entry in ARGUDB:
		datas = entry.split(":")
		if datas[0] == msgs[0]:
			print(clrTx("Target exist, update base price",'RED'))
			hit_flag += 1
			break
		hit_index+=1
	
	if hit_flag == 0:
		if f is not None:
			f.write(msg+'\n')
	else:	
		ARGUDB.pop(hit_index)
		ARGUDB.insert(hit_index,msg)
		print("*****")
		f.close()
		f = open(home+args.database,'w')
		for entry in ARGUDB:
			f.write(entry+'\n')

	f.close()

def doKillALn(number):
    index = ARGUDB.index(number)
    ARGUDB.pop(index)
    home = expanduser('~')
    f = open(home+args.database,'w')
    for entry in ARGUDB:
        f.write(entry+'\n')
    f.close()

def main():
	#doStuff(tTarget)
	if args.read :
		doDump()
	elif args.kill:
		doKillALn(tTarget)
	elif args.add:
		doWriteLn(tTarget)
	elif args.listme:
		doDumpEx()

if __name__ == '__main__':
	verify()
	refreshDb()
	main()
