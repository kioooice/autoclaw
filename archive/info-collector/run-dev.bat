@echo off
call "D:\vs\VC\Auxiliary\Build\vcvars64.bat"
set PATH=%USERPROFILE%\.cargo\bin;%PATH%
cd /d C:\Users\Administrator\.openclaw-autoclaw\workspace\info-collector
npm run tauri:dev