@echo off
chcp 65001

set "HTML_FILE=C:\Users\Administrator\Desktop\openclaw应用.html"
set "DOCX_FILE=C:\Users\Administrator\Desktop\openclaw应用.docx"
set "WPS_PATH=C:\Users\Administrator\AppData\Local\Kingsoft\WPS Office\12.1.0.25225\office6\wps.exe"

if not exist "%WPS_PATH%" (
    echo WPS not found at: %WPS_PATH%
    exit /b 1
)

echo Opening HTML in WPS...
start "" "%WPS_PATH%" "%HTML_FILE%"

echo Please manually save the file as .docx format in WPS
echo Target location: %DOCX_FILE%
pause
