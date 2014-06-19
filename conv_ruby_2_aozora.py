import os, sys, re, codecs
import argparse
import logging
import urllib, urllib2
import curses
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
from curses import panel

global DB
global tTarget
global args
global ARGUDB
global _wrap
global LINKS
global UIflag

UIflag = 1
LINKS = []
ARGUDB = []
_wrap = TextWrapper()
_wrap.width = 34

class Menu(object):                                                          

    def __init__(self, items, stdscreen):                                    
        self.window = stdscreen.subwin(0,0)                                  
        self.window.keypad(1)                                                
        self.panel = panel.new_panel(self.window)                            
        self.panel.hide()                                                    
        panel.update_panels()                                                

        self.position = 0                                                    
        self.items = items                                                                      
        self.items.append(('==== OUTPUT ==== (press "q" for exit)','nothing'))
        self.items.append(('>','nothing'))

    def navigate(self, n):                                                   
        self.position += n                                                   
        if self.position < 0:                                                
            self.position = len(self.items)-3
        elif self.position > len(self.items)-3:                               
            self.position = 0

    def display(self):                                                       
        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear()                                                  

        while True:                                                          
            self.window.refresh()                                            
            curses.doupdate()                                                            
            for index, item in enumerate(self.items):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   

                if index < len(self.items)-2:
                	msg = '%s. %s' % (str(index).zfill(2), item[0])                            
                	self.window.addstr(1+index, 1, msg, mode)                    
                else:
                	msg = '%s' % (item[0])                            
                	self.window.addstr(1+index, 1, msg, mode)                    

            key = self.window.getch()                                        

            if key in [curses.KEY_ENTER, ord('\n')]:                         
                if self.position == len(self.items)-3:                       
                    break                                                    
                elif self.position == len(self.items)-2:
                	continue
                elif self.position == len(self.items)-1:
                	continue
                else:                                                        
                	self.items.pop()
                	self.items.append((self.items[self.position][1](self.items[self.position][0]),'result'))

            elif key == curses.KEY_UP:                                       
                self.navigate(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigate(1)                                             

            elif key == ord('q'):
            	break

        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()


class MyApp(object):	
	def __init__(self, stdscreen):		
		self.screen = stdscreen
		try:
			curses.curs_set(0)
		except:
			print "don\'t support curs_set"			

		filenames = []
		for (dirpath, dirnames, filenames) in os.walk(tTarget):		
			break

		#print filenames
		#raw_input()

		if len(filenames) > 0 :
			__main_menu_items = []
			cnt = 0

			for filename in filenames:
				if cnt < 20:
					if filename[0] is not '.':
						__main_menu_items.append((filename,doSomeTrick))
				cnt+=1

			self.__main_menu = Menu(__main_menu_items, self.screen)
			self.__main_menu.display()

		else:
			self.__main_menu = Menu([], self.screen)
			self.__main_menu.display()

def doSomeTrick(filename):				
	result = 'doSomeTrick'
	f = open(filename,'r')
	if f is not None:
		content = f.read()
		result = applyTrick(filename,content)		
		f.close()
	else:
		result = 'can\'t open '+filename+'!'	
	return result

def aozoraFmtStr(rubyString):
	newString  = ''
	newString = rubyString.replace('<ruby>','') 
	newString = newString.replace('</ruby>','') 
	newString = newString.replace('<rb>','') 
	newString = newString.replace('</rb>','')
	newString = newString.replace('<rt>','\xe3\x80\x8a') 
	newString = newString.replace('</rt>','\xe3\x80\x8b')
	newString = rubyString.replace('<RUBY>','') 
	newString = newString.replace('</RUBY>','') 
	newString = newString.replace('<RB>','') 
	newString = newString.replace('</RB>','')
	newString = newString.replace('<RT>','\xe3\x80\x8a') 
	newString = newString.replace('</RT>','\xe3\x80\x8b') 
	newString = newString.replace('<BR>','\n') 
	newString = newString.replace('<br>','\n')
	newString = newString.replace('<RP>(</RP>','') 
	newString = newString.replace('<RP>)</RP>','')

	newString = newString.replace('\xe3\x80\x8a\xe3\x80\x8b','')
	return newString

def applyTrick(filename,content):
	result = 'trick applied'	
	#do some trick here		
	newContent = aozoraFmtStr(content)
	f = open('azo_'+filename,'w')
	if f is not None:
		f.write(newContent)
		f.close()
	else:
		DB.debug('can\'t open azo_'+filename+' for writing.')
	return result

def doStuff():	
	curses.wrapper(MyApp)

def doStuffDirect():
	DB.debug('Dirct execute')
	ret = doSomeTrick(tTarget)
	DB.debug(ret)

def setup_logging(level):
	global DB
	DB = logging.getLogger('conv_ruby_2_aozora') #replace
	DB.setLevel(level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
	DB.addHandler(handler)

def verify():
	global tTarget
	global args
	global UIflag
	parser = argparse.ArgumentParser(description='A conv_ruby_2_aozora Utility') #replace
	parser.add_argument('-v', '--verbose', dest='verbose', action = 'store_true', default=False, help='Verbose mode')
	parser.add_argument('query', nargs='*', default=None)
	parser.add_argument('-d', '--database', dest='database', action = 'store', default='/.hmDict/conv_ruby_2_aozora.db') #replace
	args = parser.parse_args()
	tTarget = ' '.join(args.query)	
	log_level = logging.INFO
	if args.verbose:
		log_level = logging.DEBUG
	if not tTarget:
		tTarget = os.getcwd()		
		#print tTarget
		#raw_input()
	else :
		UIflag = 0
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
	if UIflag == 1:
		doStuff()
	else:
		doStuffDirect()

if __name__ == '__main__':
	verify()
	loadDb()
	main()
