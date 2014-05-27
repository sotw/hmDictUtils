INSFOLDER=~/.hmDict
rm -Rf $INSFOLDER
rm -f ~/bin/sh/edict
rm -f ~/bin/sh/jdict
rm -f ~/bin/sh/google
mkdir -p ~/bin/sh
mkdir -p $INSFOLDER
cp -Rf jianfan $INSFOLDER
cp -Rf jNlp $INSFOLDER
cp *.py $INSFOLDER
cp edict ~/bin/sh
cp jdict ~/bin/sh
cp google ~/bin/sh
cp argumentDbA $INSFOLDER/argumentDbA
cp argumentDbB $INSFOLDER/argumentDbB
chmod 755 -R $INSFOLDER
chmod 755 -R ~/bin/sh
