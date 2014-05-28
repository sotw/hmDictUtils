INSFOLDER=~/.hmDict
rm -Rf $INSFOLDER
rm -f ~/bin/sh/edict
rm -f ~/bin/sh/jdict
rm -f ~/bin/sh/google
rm -f ~/bin/sh/wiki
mkdir -p ~/bin/sh
mkdir -p $INSFOLDER
cp -Rf jianfan $INSFOLDER
cp -Rf jNlp $INSFOLDER
cp -Rf wikipedia $INSFOLDER
cp *.py $INSFOLDER
cp edict ~/bin/sh
cp jdict ~/bin/sh
cp google ~/bin/sh
cp wiki ~/bin/sh
cp argumentDbA $INSFOLDER/argumentDbA
cp argumentDbB $INSFOLDER/argumentDbB
sudo pip install requests #for wikipedia
sudo pip install BeautifulSoup4 #for wikipedia
chmod 755 -R $INSFOLDER
chmod 755 -R ~/bin/sh
