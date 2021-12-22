chcp 65001
set PKGFOLDER="%localappdata%\hmDict"
set tPage="https://tw.dictionary.search.yahoo.com/search?p="%1
python %PKGFOLDER%/edict.py %tPage%
pause
chcp 950
