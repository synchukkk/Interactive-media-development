@echo off
REM Відкриває index.html у Google Chrome (якщо встановлено) або у браузері за замовчуванням
SETLOCAL ENABLEDELAYEDEXPANSION
SET "FILE=%~dp0index.html"

REM Спробуємо запустити chrome якщо доступний в PATH
start "" "chrome" --new-window "%FILE%"

REM Якщо попередня команда не відкрила (в деяких системах start повертає 0 одразу),
REM пробуємо відомі шляхи
IF EXIST "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --new-window "%FILE%"
  goto :eof
)
IF EXIST "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --new-window "%FILE%"
  goto :eof
)

REM Інакше відкриваємо файл у браузері за замовчуванням
start "" "%FILE%"
ENDLOCAL
