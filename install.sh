mkdir -p ~/bin/sh
mkdir -p ~/.hmDictDb
rm -f ~/bin/sh/pyYahooDictionary.py
rm -f ~/bin/sh/gooJpDictionary.py
rm -f ~/bin/sh/gooDetailA.py
rm -f ~/bin/sh/HMTXCLR.py
rm -f ~/bin/edict
rm -f ~/.hmDictDb/argumentDbA
rm -f ~/.hmDictDb/argumentDbB
rm -rf ~/bin/sh/jianfan
rm -rf ~/bin/sh/jNlp
cp -Rf jianfan ~/bin/sh
cp -Rf jNlp ~/bin/sh
cp pyYahooDictionary.py ~/bin/sh
cp gooJpDictionary.py ~/bin/sh
cp gooDetailA.py ~/bin/sh
cp HMTXCLR.py ~/bin/sh
cp edict ~/bin/sh
cp jdict ~/bin/sh
cp argumentDbA ~/.hmDictDb/argumentDbA
cp argumentDbB ~/.hmDictDb/argumentDbB
chmod 755 ~/bin/sh/edict
chmod 755 ~/bin/sh/jdict
chmod 755 ~/bin/sh/HMTXCLR.py
chmod 755 ~/bin/sh/pyYahooDictionary.py
chmod 755 ~/bin/sh/gooJpDictionary.py
chmod 755 ~/bin/sh/gooDetailA.py
