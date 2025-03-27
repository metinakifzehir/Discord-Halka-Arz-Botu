python halkarz.py
python compare.py
python dcbot.py
DEL /F /Q /A "eski.txt"
timeout /t 1
ren "halkarz.txt" "eski.txt"
DEL /F /Q /A "yeni.txt"