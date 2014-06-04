# Author Pei-Chen Tsai aka Hammer
# 2014-05-28 13:48:03

from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib2
import os, sys, re, codecs
import argparse, logging
from HMTXCLR import clrTx
from os.path import expanduser
from jianfan import jtof
from textwrap import TextWrapper
import wikipedia

global tTargetA
global DB
global LANG
global _wrap

LANG='en'
tTargetA=''
INSFOLDER=''
_wrap = TextWrapper()
_wrap.width = 80

def prettyPrint(text,LANG):
	DB.debug(text)
	sections = re.findall('([^=]+?)==',text)
	for section in sections:
		for line in _wrap.wrap(section):
			print '    '+line
		raw_input()


def getWikiContent(queryStr):
	result = ''
	#DB.debug('debug print')
	#DB.error('error!')
	wikipedia.set_lang(LANG)
	try:
		q = wikipedia.page(queryStr)
		content = ''
		if LANG == 'zh' :
			content, bChanged = jtof(q.content)
		else:
			content = q.content
		result = content
		DB.debug(result)
	except wikipedia.exceptions.DisambiguationError as e :		
		DB.error(e)
	except wikipedia.exceptions.PageError as e:	
		DB.error(e)
	return result

def main():
	result = getWikiContent(tTargetA)
	#print resultSet
	prettyPrint(result,LANG)

def setup_logging(level):
	global DB
	DB = logging.getLogger('pyWiki')
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTargetA
	global LANG
	parser = argparse.ArgumentParser(description='A wikipedia wrapper for my own purpose')
	parser.add_argument('-l', '--language', dest='language', action='store', default='en', help='Language mode')
	parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None )
	args = parser.parse_args()
	query = ' '.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	if not query:
		parser.print_help()
		exit()	
	LANG = args.language
	tTargetA = query
	setup_logging(log_level)
	DB.debug(args.language)
	return

if __name__ == '__main__':
	verify()
	main()
