mkdir -p ~/bin/sh
mkdir -p ~/.hmDictDb
rm -f ~/bin/sh/pyYahooDictionary.py
rm -f ~/bin/sh/HMTXCLR.py
rm -f ~/bin/edict
rm -f ~/.hmDictDb/argumentDbA
cp pyYahooDictionary.py ~/bin/sh
cp HMTXCLR.py ~/bin/sh
cp edict ~/bin/sh
cp argumentDbA ~/.hmDictDb/argumentDbA
chmod 755 ~/bin/sh/edict
chmod 755 ~/bin/sh/HMTXCLR.py
chmod 755 ~/bin/sh/pyYahooDictionary.py
