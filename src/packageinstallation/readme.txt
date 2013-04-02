On any OS:
First download python2.7 and make a note of where it installs to


Windows:
Run winpackageinstaller.py
Unix/Mac:
Run unixpackageinstaller.py

This will put distribute and pip 
on your computer. These two packages allow easy installation of
other python packages. This script also searches for the python dir
and runs a batch file to install packages with pip. You should be able
to just download python2.7 and run this script and be set. If .py 
isn't associated with any program, navigate to your python2.7 install
directory and run it with python.exe

This script is guaranteed to download 'distribute' and 'pip' but 
may not correctly find pip and execute shell commands correctly,
especially for Unix/Mac. If that is the case, open your shell 
(or command prompt) and change directory (cd) to python\scripts
then install the packages. Below is the windows batchfile, I would
just copy the second and third lines in after getting to the correct 
directory. 
cd C:\Python27\scripts\
pip install matplotlib numpy scipy pypdf sphinx reportlab
pip install http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.6/basemap-1.0.6.tar.gz/download