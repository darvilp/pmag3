'''
Created in March 2013
Defines a paleomag function for the GUI so pmag3 doesn't have all of this stuck in it. 
'''

'''
Created on January 19, 2013

@author: payne
Daniel Payne, SUNY GENESEO
dap11@geneseo danielarvilpayne@gmail.com
v1.5:
This script takes a .txt file from the JR6 magnetometer and outputs another space delimited textfile that contains
only the parts that we use. The output file has a .dmg extension because that is what we were using before. 
To use this script, just run it in the directory with your textfiles. Make sure there are 22 lines between each of the entries in your textfiles.  
This is written for Python 2.7, so if nothing happens or errors come up, check and make sure the default python is 2.7 and not 3.x
I am going to go heavy on the comments and explain all of the functions to increase legibility. 
In changing this from the drag and drop version to the directory searching version, some parts have been taken out with
comments.
If column labels are not wanted, put a # infront of line 165 
The whole .drm thing is half pointless now though, since I just keep modifying this to do what was otherwise needed. 

v2.0: In v2.0 the script will be broken up into modules and a GUI is going to be created.
TODO: make modules-Mostly done?
GUI
Portability-Windows is good, Mac has trouble with basemap
fix ellipses
rewrite some of the data input to make things smoother and more professional
Testing
'''
# import statements, imports libraries of functions
import os
'''
import math
import pylab
from matplotlib.patches import Ellipse
from mpl_toolkits.basemap import Basemap
import stereoplot
import coreanalysis
import siteanalysis
import haversine
'''
def paleomag2(currentdir):
    n = 0
    filepath = []  # creates lists. A list only exists in the area where it was created, so if it is no tabs in like these are, the list exists throughout the entire program, while if it was one tab in it only exists in that smaller section of the code.
    textfilename = []
    # this loop thing finds all of the files in the directory with .txt in their nameand adds their names (e.g VA12-05A.txt) to a list
   
    for files in os.listdir(currentdir):
        if files.endswith(".txt"):
            filepath.append(files)
    textfilename = filepath  # Since things changed from previous versions, this is a quick fix to let the old program be used for multiple files the way that I've done it
    sites = []  # these are the names of the sites
    for n in range(0, len(filepath)):  # this loop takes the first 7 characters of the textfile names and stores them in the sites list
        foo = filepath[n].__getslice__(0, 7) 
        sites.append(foo)
    cores = []
    for n in range(0, len(filepath)):  # this loop takes the first 7 characters of the textfile names and stores them in the sites list
        foo = filepath[n].__getslice__(0, 8) 
        cores.append(foo)
    sites = list(set(sites))  # this removes the duplicates in the list 
    longslist = []  # more lists that need to be made
    latslistr = []  
    dmslist = []
    dpslist = []
    si = 0  
    Dmsitelist = []
    Imsitelist = []    
    # this loop puts the whole file path infront of the names that were found in the last loop above 
    
    for n in range (0, len(filepath)):
        filepath[n] = currentdir + filepath[n]
    
    return sites, filepath, textfilename, cores,
    '''
    # Basic control flow  in this program: Two tabs in deals with individual cores e.g. VA12-05A, one tab in deals with a site e.g. VA12-05, and no tabs in deals with the entire suite e.g. VA12 
    for si in range(0, len(sites)):    
        NSSUM = 0
        EWSUM = 0
        UDSUM = 0
        CoreDmslist = []
        CoreImslist = []
        Rlist = []
        coresinsitelist = []  # this doesn't do anything,but I thought it would be useful to have
        N = 0    
        for i in range (0, len(filepath)):  # this is the loop that starts each individual file, so once one file is done it goes to the next.
            coreanalysis.coreanalysis(si, sites, filepath, i, coresinsitelist, textfilename, maxerror, cores, maxangler, EWSUM, NSSUM, UDSUM, CoreDmslist, CoreImslist)
        # This is all of the math for the individual sites.Everything should be self explanatory
        siteanalysis.siteanalysis(sites, si, CoreDmslist, CoreImslist, Dmsitelist, Imsitelist, coresinsitelist, dmslist, latslistr, dpslist, longslist)
        
    latslist = []
    for n in range(0, len(latslistr)):
        latslist.append(math.degrees(latslistr[n]))
    
    # Map plotting section
    
    
    # Makes the map. If a different projection is wanted, change m= basemap. npstere exists and might be wanted intstead of stere
    # m = Basemap(projection='npstere',boundinglat=60,lon_0=90,round=True)
    m = Basemap(projection='ortho', lon_0=0, lat_0=90, resolution='l')
    fig = pylab.figure(figsize=(15, 5))
    m.drawcoastlines()
    m.fillcontinents(color='coral', lake_color='aqua')  # draw parallels and meridians.
    m.drawparallels(pylab.arange(-80., 81., 20.))
    m.drawmeridians(pylab.arange(-180., 181., 20.))
    m.drawmapboundary(fill_color='aqua') 
    
    # draw ellipses
    for n in range(0, len(longslist)):
        xy = m(longslist[n], latslist[n])
        w = haversine.haversine(longslist[n] - dmslist[n], latslist[n], longslist[n] + dmslist[n], latslist[n])
        h = haversine.haversine(longslist[n], latslist[n] - dpslist[n], longslist[n], latslist[n] + dpslist[n])
        e = Ellipse(xy, w, h, longslist[n])
        pylab.gca().add_patch(e)
    
    sitesstring = ''
    for n in range(0, len(sites)):
        sitesstring = sites[n] + ',' + sitesstring
    pylab.title("North Pole Stereographic Projection of " + sitesstring)
    pylab.savefig("Paleoplot of " + sitesstring + ".png")
    pylab.show(block=False)
    
    stereoplot.stereoplot(Dmsitelist, Imsitelist, sites)
    pylab.show()

     '''
