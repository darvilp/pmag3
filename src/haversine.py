'''
Created on Jan 21, 2013

@author: payne
'''
import math
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