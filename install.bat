@echo off
REM []== Can we just ignore .bat?
REM []== I should write all stuff in vbs.
set EXEFOLDER="%UserProfile%\bin\bat"
set INSFOLDER="%localappdata%\hmDict"
set SRCFOLDER="%cd%"

rmdir /S /Q %INSFOLDER%

mkdir %EXEFOLDER%
cd %EXEFOLDER%
del /F /Q edict.bat
del /F /Q jdict.bat
del /F /Q google.bat
del /F /Q wiki.bat
del /F /Q getPOEReleaseNote.bat
del /F /Q get_taipei_times.bat
del /F /Q get_lyrics.bat
del /F /Q get_jpnews.bat
cd %SRCFOLDER%
mkdir %INSFOLDER%
xcopy jianfan %INSFOLDER%\jianfan /E /I
xcopy jNlp %INSFOLDER%\jNlp /E /I
xcopy wikipedia %INSFOLDER%\wikipedia /E /I

xcopy *.py %INSFOLDER%
xcopy *.bat %EXEFOLDER%

xcopy argumentDbA %INSFOLDER%
xcopy argumentDbB %INSFOLDER%
xcopy *.db %INSFOLDER%

pip install requests
pip install BeautifulSoup4
pip install chardet

cd %EXEFOLDER%
del /F /Q install.bat
cd %SRCFOLDER%

echo Current PATH is:
echo %PATH%

set /p ANSWER=Do you wan to set %EXEFOLDER% in PATH(Y//N)?
echo You choose: %ANSWER%
IF /I %ANSWER%==y goto :yes
IF /I %ANSWER%==yes goto :yes
goto :finish

:yes
echo writting registry...
writePath.vbs %EXEFOLDER%
REM set PATH=%PATH%;%EXEFOLDER%

:finish
echo []== Done, have a nice day.
pause