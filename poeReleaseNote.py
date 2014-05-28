import os, sys, re, codecs
import argparse
import logging
import urllib, urllib2
from subprocess import PIPE
from subprocess import Popen
from lxml import etree
from cStringIO import StringIO
from pprint import pprint

global DB
global tTarget

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
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')
	for li in tree.xpath("//li"):
		li.tail = 'breakHere' + li.tail if li.tail else 'breakHere'
	etree.strip_tags(tree,'li')
	for strong in tree.xpath("//strong"):
		strong.tail = 'breakHere' + strong.tail if strong.tail else 'breakHere'
	etree.strip_tags(tree,'strong')
	etree.strip_tags(tree,'span')
	etree.strip_tags(tree,'ul')
	etree.strip_tags(tree,'br')

	resultSet = tree.xpath("//div[@class='content']")
	#print len(resultSet)
	for entry in resultSet:
		if entry.text is not None:
			result = entry.text.replace('breakHere','\n')
			print result
			break #first post is releasenote

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
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(data), parser)
	result = etree.tostring(tree.getroot(), pretty_print=True, method="html", encoding='utf-8')

	releaseNoteSet = re.findall('<div class="title"><a href="([^"]+)">([^<]+)</a',result)
	cnt = 0
	for e in releaseNoteSet:
		print "SN:%d|%s"%(cnt,e[1])
		cnt+=1
	sn=None
	sn=raw_input('Which one you want to check?(Sn)')
	sn = parseInt(sn)
	if sn is not None:
		getReleaseNoteDetail('http://www.pathofexile.com'+releaseNoteSet[sn][0])
	return

def setup_logging(level):
	global DB
	DB = loggin.getLogger('releasenote')
	DB.setLevel(level)
	handler = loggin.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	parser = argparse.ArgumentParser(description='A poe information reader in console')
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	args = parser.parse_args()
	tTarget = ' '.join(args.query)
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	if not tTarget:
		parser.print_help()
		exit()
	

def main():
	doStuff(tTarget)

if __name__ == '__main__':
	verify()
	main()
