### A Tool Set for playing Python

> In console, you put your fingure on mouse, and you lose.

Seriously, this tool set is just to satisfy personal ambitious
to write down an idea in code **immediately** no mater how stupid it is.
You can use/modify it without my permission.
Feedback is welcome all the time.
Fork/Pull request is even better.

##### After 8 years, I decide to renew these project from python2 to python3

##### Install

This is almost 8 years project, I used to have lots operating system, now I only use ubuntu and it's spin off pop os

```bash
./install_ubuntu.sh
```

##### Update

you don't have to install packge everytime

```bash
./update_ubuntu.sh
```

##### How to use

In network reachable environment:

**edict** "word" | for consulting English dictionary.  Status : moved to single repository

> This is for Taiwanese or HK ppl\(And those who use Traditional Chinese as native language\)
> 
> 2021 : Since this my very first project, I put it on single repository and remove from here.

**jdict** "word" | for consulting Japanese dictionary.

> Not working currently

**wiki** -l "language" "word" | for consulting wiki | broken

> For example : wiki -l jp "はな"

**google** "word" | for google | broken

> Just google it.

**getPOEReleaseNote** | for fun | broken

> POE | Path of Exile

**get_taipei_times** | for read | working on python3

> Bring you back to reality.

**get_lyrics** | for music | metro lyrics went offline thus this is not working | move to legacy

> Get lyrics !

**get_jpnews** | for Japanese News | broken

> Read News !

**note** | a simple note | broken

> Note stuff !

**get_ted_talk_science** | for science! | broken

> Read ideas!

**download_linux_kernel** | for kernel compile | broken

> Hello, nerd!

**get_icrt_top_song** | just list | broken

> But I found I am interesting what DJ play more than top list.

**udict** "word" | some ted speech will need this to consult | working on python2

> lousy urban word always has its own meanings different from dictionary

**get_ign_topstory | read game news is nerd standard. | broken

> I blame game industry, the manual become so slim, I can't even call it manual "book" now, it's manual paper.

**treeMurder** | travel file system and kill some specific folders.(Currently I use it to delete .git .repo folders for release sake) | broken

##### Idea

1. Move to Python3 (the end of 2021)

##### History Idea

1. ~~Need to accept space in **edict** ok, use argparse module will solve the problem~~ 2014-06-07
2. Add language(c/c++) reference check util, hum, **cdict** maybe?
3. ~~You will need phonetic symbol in **edict**~~ 2014-05-30 12:47:45
4. I am thinking of consulting multiple pdf file in real time.
5. ~~**enews**~~ Now you have taipei times, it's ok for headline read.
6. **jnews**
7. ~~**google** google consult~~ now you can google until ajax api is ceased.
8. **gmailReader**
9. Adopt python module argparse...40% ...actually I want to keep my old fashion way in one of tool
10. Adopt python module logging...40%
11. ~~wiki~~ done!, it looks ugly for showing.
12. maybe read PDF text?
13. make a urban English consulting utility
14. osx can use 'say' to do TTS
15. ~~A lyrics search utility~~
16. ~~TED script fetch~~ done! 2014-06-05 15:46:00
17. A stackoverflow console search
18. get\_Lyrics should work with moc, music on console
19. some remark feature in reading would be amazing.
20. a loop for multiple consulting would be handy (edict/jdict)
21. a console showing mechanism that input country name and show world map.
22. output aozora style text of all Japanese text, because I need Hiragana mark.
23. make get\_ted\_talk\_science become get\_ted\_talk and list all possible when user is not input category
24. ~~write a linux kernel downloader~~ It could be more nerdy, if I fetch more version.
25. ~~remove note database to dropbox folder.~~ I just put a option in install.sh it works.
26. expand color!
27. google img fetcher. 
    prototype A. download 9 images once B. combine them as 1 3x3 big image C. display them D. downloadable for each one.
28. I should make note can extend subject. like 1 .. 1-1 1-1-1 1-1-2 1-2
29. make a really simple utility to read facebook feed and replay it in console , I have old implementation, should be easy for me.
30. ok, I hope I have a simple terminal python that can list files or directory and I can choose one to manipulate to do something.
31. I will need a simple tool that doing ruby web tag to aozora format.
32. I need to know verb tense as well. for edict
33. ~~Added urban dictionary~~

##### Note

1. Plan to use jNlp
   
   > Maybe just use hiraganamegane
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
15. [linux kernel](https://www.kernel.org)
16. [wordhippo](http://www.wordhippo.com) consult tense!
