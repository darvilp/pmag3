from matplotlib.patches import Polygon, Ellipse 
import matplotlib.pyplot as plt
import numpy as np 
import math 
from mpl_toolkits.basemap import Basemap
'''
map = Basemap(projection='npstere',boundinglat=60,lon_0=90,round=True)
fig = plt.figure(figsize=(15,5))
''' '''
m = Basemap(width=12000000, height=8000000, resolution='l', projection='stere',
            lat_ts=0, lat_0=90, lon_0=-107.)''' '''
def haversine(start_long,start_latt, end_long,end_latt):
    
    d_latt = end_latt - start_latt  
    d_long = end_long - start_long
    a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2  
    c = 2 * math.asin(math.sqrt(a))  
    return 6371 * c * 1000 
w = haversine(270,60,60,60)
lat=60
longi = 0
dp=5 #h
dm=5 #w
longplusdp=longi
latplusdp=lat+dp
if lat+dp>90:
    latplusdp = 90-(lat+dp-90)
    longplusdp = longi+180
    print latplusdp
#p = Polygon([(longi-dm, lat), (longplusdp, latplusdp),(longi+dm, lat), (longi, lat-dp)])
xy= map(30,80)
print map(30,85)
print map(30,75) 
#w = 100000
h = 200000
e = Ellipse(xy, w,h,-30,)
plt.gca().add_patch(e)
''' '''
map.drawgreatcircle(longi-dm, lat, longplusdp, latplusdp) #left point to top point
map.drawgreatcircle(longplusdp, latplusdp, longi+dm, lat) #top to right
map.drawgreatcircle(longi+dm, lat, longi, lat-dp) #right to bottom
map.drawgreatcircle(longi, lat-dp, longi-dm, lat) #bottom to left
''' '''
 

map.drawcoastlines() 
#map.fillcontinents()
map.drawmapboundary() 
plt.show()'''

#stere: area preserved shape not
#ortho shape preserved area not

#llcrnrlon=0,llcrnrlat=-90,ucrnrlon=180,urcrnrlat=90, lon_0=0,lat_0=0,
m = Basemap(projection='ortho',lon_0=0,lat_0=90, resolution='l')
#m = Basemap(projection='aeqd',lat_0=0,lon_0=0)
#25000000 seems to be magic number for width and height., stuff times 10^8
#m = Basemap(projection='npstere',boundinglat=45,lon_0=0,resolution='l')
#m = Basemap(llcrnrlon=-89,llcrnrlat=-89,urcrnrlon=89,urcrnrlat=89,projection='stere',lon_0=0,lat_0=0,resolution='l')
m = Basemap(width=12000000,height=8000000,projection='stere',lon_0=0,lat_0=90,resolution='l')

#m = Basemap(llcrnrlon=-89,llcrnrlat=-89,urcrnrlon=89,urcrnrlat=89,\
 #           resolution='l',projection='laea',\
  #          lat_ts=50,lat_0=50,lon_0=-107.)
#m = Basemap(projection='ortho',lon_0=-105, lat_0=0,resolution='l') #Works, looks like ortho
#fig = plt.figure(figsize=(15,5))
#m.drawcoastlines()    
#m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.

m.drawparallels(np.arange(-90.,90.,10))
m.drawmeridians(np.arange(-180.,180.,10))
m.drawcoastlines(linewidth=1, color='k', antialiased=1, ax=None, zorder=None)
m.drawmapboundary(fill_color='white') 

def haversine(start_long,start_latt, end_long,end_latt):#finds great circle distance. Angles are inputted in degrees
    start_long=math.radians(start_long)
    start_latt=math.radians(start_latt)
    end_long=math.radians(end_long)
    end_latt=math.radians(end_latt)
    d_latt = end_latt - start_latt  
    d_long = end_long - start_long
    a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2  
    c = 2 * math.asin(math.sqrt(a))  
    return 6371 * c *1000

longslist=[0,90,180]
latslist=[65,65,65]
dpslist=[5,10,5]
dmslist=[5,5,10]
print m(0,60)
print m(0,70)
print m(-5,65)
print m(5,65)
print m.gcpoints(0,60,0,70,10)

m.drawgreatcircle(0,60,0,70,100)
m.drawgreatcircle(-5,65,5,65,100)

m.drawgreatcircle(0,60,-5,65,100)
m.drawgreatcircle(0,60,5,65,100)

m.drawgreatcircle(-5,65,0,70,100)
m.drawgreatcircle(0,70,5,65,100)
'''
# draw ellipses
for n in range(0,len(longslist)):
    xy= m(longslist[n],latslist[n])
    w = haversine(longslist[n]-dmslist[n],latslist[n],longslist[n]+dmslist[n],latslist[n])
    h = haversine(longslist[n],latslist[n]-dpslist[n],longslist[n],latslist[n]+dpslist[n])
    e = Ellipse(xy, w,h,longslist[n])
    print xy, w,h,e
    plt.gca().add_patch(e)'''
plt.show()