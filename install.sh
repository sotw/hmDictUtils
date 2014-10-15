INSFOLDER=~/.hmDict
echo "If you are mac user, please use mac port"
echo "http://www.macports.org/"
echo "And download both python and pip"
echo "And don't forget set PATH for ~/bin/sh all wrapped bash script is there"
rm -Rf $INSFOLDER
rm -f ~/bin/sh/run_meld
rm -f ~/bin/sh/edict
rm -f ~/bin/sh/jdict
rm -f ~/bin/sh/udict
rm -f ~/bin/sh/google
rm -f ~/bin/sh/wiki
rm -f ~/bin/sh/getPOEReleaseNote
rm -f ~/bin/sh/get_taipei_times
rm -f ~/bin/sh/get_lyrics
rm -f ~/bin/sh/get_jpnews
rm -f ~/bin/sh/note
rm -f ~/bin/sh/get_ted_talk
rm -f ~/bin/sh/download_linux_kernel
rm -f ~/bin/sh/get_icrt_top_song
rm -f ~/bin/sh/conv_ruby_2_aozora
rm -f ~/bin/sh/get_ign_topstory
rm -f ~/bin/sh/get_ign_review
rm -f ~/bin/sh/get_stock
rm -f ~/bin/sh/arcProductManager
rm -f ~/bin/sh/ssh_to_mephi
rm -f ~/bin/sh/treeMurder
mkdir -p ~/bin/sh
mkdir -p $INSFOLDER
cp -Rf jianfan $INSFOLDER
cp -Rf jNlp $INSFOLDER
cp -Rf wikipedia $INSFOLDER
#cp -Rf uniseg $INSFOLDER
cp *.py $INSFOLDER
cp run_meld ~/bin/sh
cp edict ~/bin/sh
cp jdict ~/bin/sh
cp udict ~/bin/sh
cp google ~/bin/sh
cp wiki ~/bin/sh
cp getPOEReleaseNote ~/bin/sh
cp get_taipei_times ~/bin/sh
cp get_lyrics ~/bin/sh
cp get_jpnews ~/bin/sh
cp get_ted_talk ~/bin/sh
cp get_icrt_top_song ~/bin/sh
cp conv_ruby_2_aozora ~/bin/sh
cp get_ign_topstory ~/bin/sh
cp get_ign_review ~/bin/sh
cp get_stock ~/bin/sh
cp arcProductManager ~/bin/sh
cp -f ssh_to_mephi ~/bin/sh
cp treeMurder ~/bin/sh
echo "Do you want to use Dropbox folder as your note/get_stock database?"
select yn in "Yes" "No"; do
	case $yn in
		Yes ) cp noteDropbox ~/bin/sh/note;cp get_stockDropbox ~/bin/sh/get_stock;break;;
		No ) cp note ~/bin/sh; cp get_stock ~/bin/sh;break;;
	esac
done
cp download_linux_kernel ~/bin/sh
cp argumentDbB $INSFOLDER/argumentDbB
cp *.db $INSFOLDER
echo "Do you use mac and need a fresh install for pip?"
select yn in "Yes" "No"; do
	case $yn in
		Yes ) sudo easy_install pip; break;;
		No ) echo "skip easy_install pip"; break;;
	esac
done
echo "Do you use mac and need a port install lxml?"
select yn in "Yes" "No"; do
	case $yn in
		Yes ) sudo port install py27-lxml; sudo pip install lxml; break;;
		No ) echo "skip install py27-lxml"; break;;
	esac
done
#I should seperate this to python deploy
#sudo pip install re #for wikipedia
sudo pip install BeautifulSoup4 #for wikipedia
sudo pip install chardet #for goojp
sudo pip install Skype4Py
sudo pip install pdfminer

echo "Are you using opensuse and need lxml module for python?"
select yn in "Yes" "No"; do
	case $yn in
		Yee ) sudo zypper install python-lxml; break;;
		No ) echo "You are welcome to feed"; break;;
	esac
done

chmod -R 755 $INSFOLDER
chmod -R 755 ~/bin/sh

echo "Do you want to add PATH envirnment in .bashrc?(restart terminal will effect at once)"
select yn in "Yes" "No"; do
	case $yn in
		Yes ) echo "PATH=$PATH:~/bin/sh:~/bin" > ~/.bashrc; break;;
	    No ) google have a nice day; break;;
	esac
done
