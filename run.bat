for %%* in (.) do set CurrDirName=%%~nx*
docker kill %CurrDirName%
docker rm %CurrDirName%
docker run --name %CurrDirName% -p 8000:80 -v %~dp0/src:/src^
 python/%CurrDirName%