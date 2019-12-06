@ECHO OFF

FOR /L %%y IN (1, 1, 7) DO CALL :phonebill
EXIT /B %ERRORLEVEL% 

:phonebill
cd ./HSBC
py -m pytest
cd ../
TIMEOUT /T 120 /NOBREAK

cd ./DBS
py -m pytest
cd ../
TIMEOUT /T 120 /NOBREAK

EXIT /B 0