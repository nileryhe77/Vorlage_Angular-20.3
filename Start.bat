@echo off

rem Öffnet das erste Konsolenfenster und aktiviert das Virtual Environment
start cmd /k "call cd python && venv\Scripts\activate && py -m application.main"


rem Wartet eine kurze Zeit, um sicherzustellen, dass das erste Fenster geöffnet ist
timeout /t 2 /nobreak



rem Öffnet ein zweites Konsolenfenster, wechselt in das agular Verzeichnis und startet npm
start cmd /k "cd angular && ng serve --ssl --ssl-key localhost.key --ssl-cert localhost.crt"