INSFOLDER=~/.hmDict
echo "If you are mac user, please use mac port"
echo "http://www.macports.org/"
echo "And download both python and pip"
rm -Rf $INSFOLDER
rm -f ~/bin/sh/edict
rm -f ~/bin/sh/jdict
rm -f ~/bin/sh/google
rm -f ~/bin/sh/wiki
rm -f ~/bin/sh/getPOEReleaseNote
rm -f ~/bin/sh/getTaipeiTimes
rm -f ~/bin/sh/get_lyrics
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
cp getPOEReleaseNote ~/bin/sh
cp getTaipeiTimes ~/bin/sh
cp get_lyrics ~/bin/sh
cp argumentDbA $INSFOLDER/argumentDbA
cp argumentDbB $INSFOLDER/argumentDbB
cp *.db $INSFOLDER
sudo pip install requests #for wikipedia
sudo pip install BeautifulSoup4 #for wikipedia
sudo pip install chardet #for goojp
chmod -R 755 $INSFOLDER
chmod -R 755 ~/bin/sh
