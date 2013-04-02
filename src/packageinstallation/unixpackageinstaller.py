'''
Created on Feb 1, 2013

This python script works in conjunction with pip to automatically download
and install the packages that paleomag2.0 uses. 
@author: payne
'''
import urllib2


# downloads and installs distribute
u = urllib2.urlopen('http://python-distribute.org/distribute_setup.py')  # downloads
localFile = open('distribute_setup.py', 'w')  # opens a local file named for distribute
localFile.write(u.read())  # writes distribute to the file
localFile.close()  # closes the file
# runs the local file distribute_setup.py

# downloads get-pip.py from github URL. If get-pip changes in the future, make sure this
# line has raw.github, otherwise you'll get an html document.
# after download, the file is opened locally and then ran
u = urllib2.urlopen('https://raw.github.com/pypa/pip/master/contrib/get-pip.py')
localFile = open('get-pip.py', 'w')
localFile.write(u.read())
localFile.close()



import sys
print sys.executable
pipscript = open("unixscript.sh", 'w')
pipscript.writelines('cd ' + sys.executable.rstrip('python.exe') + "/scripts\n")  # note that unix uses forward slash for paths
pipscript.writelines('pip install  numpy scipy matplotlib ipython pypdf sphinx reportlab\n')
pipscript.writelines('pip install http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.6/basemap-1.0.6.tar.gz/download')
pipscript.close()

import subprocess
subprocess.call([sys.executable, 'distribute_setup.py'])
subprocess.call([sys.executable, 'get-pip.py'])
subprocess.call(['sudo', '-s', 'sh', 'unixscript.command'], shell=True)  # tries running in its own shell
# subprocess.call(['sudo','./unixscript.sh'], shell=True)#tries with bash
