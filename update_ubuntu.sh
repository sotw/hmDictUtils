INSFOLDER=~/.hmDict
rm -Rf $INSFOLDER
rm -f ~/bin/sh/edict
rm -f ~/bin/sh/jdict
rm -f ~/bin/sh/udict
rm -f ~/bin/sh/google
rm -f ~/bin/sh/wiki
rm -f ~/bin/sh/getPOEReleaseNote
rm -f ~/bin/sh/get_taipei_times
rm -f ~/bin/sh/get_lyrics
rm -f ~/bin/sh/get_jpnews
rm -f ~/bin/sh/get_8muse
rm -f ~/bin/sh/note
rm -f ~/bin/sh/get_ted_talk
rm -f ~/bin/sh/download_linux_kernel
rm -f ~/bin/sh/get_icrt_top_song
rm -f ~/bin/sh/conv_ruby_2_aozora
rm -f ~/bin/sh/get_ign_topstory
rm -f ~/bin/sh/get_ign_review
rm -f ~/bin/sh/get_stock
rm -f ~/bin/sh/treeMurder
rm -f ~/bin/sh/batchRename
mkdir -p ~/bin/sh
mkdir -p $INSFOLDER
cp -Rf jianfan $INSFOLDER
cp -Rf jNlp $INSFOLDER
cp -Rf wikipedia $INSFOLDER
#cp -Rf uniseg $INSFOLDER
cp *.py $INSFOLDER
cp edict ~/bin/sh
cp jdict ~/bin/sh
cp udict ~/bin/sh
cp google ~/bin/sh
cp wiki ~/bin/sh
cp getPOEReleaseNote ~/bin/sh
cp get_taipei_times ~/bin/sh
cp get_8muse ~/bin/sh
cp get_lyrics ~/bin/sh
cp get_jpnews ~/bin/sh
cp get_ted_talk ~/bin/sh
cp get_icrt_top_song ~/bin/sh
cp conv_ruby_2_aozora ~/bin/sh
cp get_ign_topstory ~/bin/sh
cp get_ign_review ~/bin/sh
cp get_stock ~/bin/sh
cp treeMurder ~/bin/sh
cp batchRename ~/bin/sh
cp download_linux_kernel ~/bin/sh
cp argumentDbB $INSFOLDER/argumentDbB
cp *.db $INSFOLDER

chmod -R 755 $INSFOLDER
chmod -R 755 ~/bin/sh

