###A Tool Set for Everyday Reading and Writing in Console only
>In console, you put your fingure on mouse, you lose.

##### Install
	execute ./install.sh

##### How to use
In network reachable environment:

**edict** "word" | for consulting English dictionary.
>This is for Taiwanese or HK ppl\(And those who use Traditional Chinese as native language\)

**jdict** "word" | for consulting Japanese dictionary.
>This is for Everyone

**wiki** -l "language" "word" | for consulting wiki
>For example : wiki -l jp "はな"

**google** "word" | for google
>Just google it.

**getPOEReleaseNote** | for fun
>POE | Path of Exile

**get_taipei_times** | for read
>Bring you back to reality.

**get_lyrics** | for music
>Get lyrics !

**get_jpnews** | for Japanese News
>Read News !

**note** | a simple note
>Note stuff !

**get_ted_talk_science** | for science!
>Read ideas!

##### Idea
1. ~~Need to accept space in **edict** ok, use argparse module will solve the problem~~ 2014-06-07
2. Add language(c/c++) reference check util, hum, **cdict** maybe?
3. ~~You will need phonetic symbol in **edict**~~ 2014-05-30 12:47:45
4. I am thinking of consulting multiple pdf file in real time.
5. **enews**
6. **jnews**
7. **google** google consult
8. **gmailReader**
9. Adopt python module argparse...30% ...actually I want to keep my old fashion way in one of tool
10. Adopt python module logging...30%
11. ~~wiki~~ done!, it looks ugly for showing.
12. maybe read PDF text?
13. make a urban English consulting utility
14. osx can use 'say' to do TTS
15. ~~A lyrics search utility~~
16. ~~TED script fetch~ done! 2014-06-05 15:46:00
17. A stackoverflow console search
18. get\_Lyrics should work with moc, music on console
19. some remark feature in reading would be amazing.
20. a loop for multiple consulting would be handy (edict/jdict)
21. a console showing mechanism that input country name and show world map.
22. output aozora style text of all Japanese text, because I need Hiragana mark.
23. make get\_ted\_talk\_science become get\_ted\_talk and list all possible when user is not input category

##### Note
1. Plan to use jNlp
>Maybe just use hiraganamegane
2. Currently all pull, any push utility like blog push maybe?
3. Just dont't push so frequently. 

##### Reference
1. [Python like parseInt](http://d.hatena.ne.jp/cupnes/20110201/1296574516)
2. [Jian to Fan convert](https://code.google.com/p/python-jianfan/)
3. [pygoogle](https://code.google.com/p/pygoogle/)
4. [xgoogle](http://www.catonmat.net/blog/python-library-for-google-search/)
5. [Mecab](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html)
6. [Wikipedia, a python parser](https://github.com/goldsmith/Wikipedia)
7. [Wordpress xmlrpc](https//github.com/maxcutler/python-wordpress-xmlrpc)
8. [PDFMiner](http://www.unixuser.org/~euske/python/pdfminer/index.html)
9. [python-docx](https://github.com/mikemaccana/python-docx)
10. [Path of Exile](https://www.pathofexile.com)
11. [uniseg](http://www.emptypage.jp/gadgets/uniseg.ja.html)
12. [xjp2](http://misyakudouji.blog55.fc2.com/blog-entry-455.html)
13. [aozora4reader](https://github.com/takahashim/aozora4reader/)
14. [TED](www.ted.com)
