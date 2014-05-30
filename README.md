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

##### Idea
1. Need to accept space in **edict** ok, use argparse module will solve the problem
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
16. TED script fetch
17. A stackoverflow console search
18. get\_Lyrics should work with moc, music on console
19. some remark feature in reading would be amazing.
20. a loop for multiple consulting would be handy (edict/jdict)

##### History
1. 2014-05-30 10:51:26 change getTaipeiTimes to get\_taipei\_times

##### Note
1. Plan to use jNlp
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
