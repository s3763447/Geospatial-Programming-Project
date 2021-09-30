@echo off
call "C:\Program Files\QGIS 3.20.1\bin\o4w_env.bat"
call "C:\Program Files\QGIS 3.20.1\etc\preremove\python3-pyqt5.bat"
call "C:\Program Files\QGIS 3.20.1\etc\ini\python3.bat"

@echo on
pyrcc5 -o resources.py resources.qrc