REM We inherit Python environment from Kodi, reset it before running.
set PYTHONHOME=
set PYTHONOPTIMIZE=
set PYTHONPATH=
REM Debugging call that leaves the command lines visible
REM start cmd /k C:\Python27\python.exe C:\Utils\BDPlayLister\bdplaylister.py %*
start /b cmd /c C:\Python27\python.exe C:\Utils\BDPlayLister\bdplaylister.py %*
timeout /T 10