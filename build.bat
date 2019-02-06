for %%* in (.) do set CurrDirName=%%~nx*
docker build -t python/%CurrDirName%:latest .