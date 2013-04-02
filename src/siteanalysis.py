'''
Created on Jan 20, 2013

@author: payne
'''
import math
def siteanalysis(sites,si,CoreDmslist,CoreImslist,Dmsitelist,Imsitelist,coresinsitelist,dmslist,latslistr,dpslist,longslist):
    print 'Enter site '+sites[si]+' latitude in degrees'
    sitelat= input() #deg      
    sitelatr=math.radians(sitelat)    
    print 'Enter site '+sites[si]+' longitude in degrees'
    sitelong= input() #deg 
    sitelongr=math.radians(sitelong)
    
    #R=math.sqrt(NSSUM*NSSUM+EWSUM*EWSUM+UDSUM*UDSUM)#these big sums are done earlier during the core calculations.#this method of calculating R has been replaced with a unit vector method
    nsunittotal=0
    ewunittotal=0    
    udunittotal=0
    for foo in range(0,len(CoreDmslist)):
        nsunittotal=math.cos(CoreDmslist[foo])*math.cos(CoreImslist[foo])+nsunittotal
        ewunittotal=math.cos(CoreImslist[foo])*math.sin(CoreDmslist[foo])+ewunittotal
        udunittotal=math.sin(CoreImslist[foo])+udunittotal
    R=math.sqrt(nsunittotal*nsunittotal+ewunittotal*ewunittotal+udunittotal*udunittotal)
    #R=sum(Rlist)
    
    
    '''
    Nsn=NSSUM/R
    Ewn=EWSUM/R
    Udn=UDSUM/R
    '''
    Nsn=nsunittotal/R
    Ewn=ewunittotal/R
    Udn=udunittotal/R 
 
    Dm = math.atan2(Ewn, Nsn)
    Im = math.asin(Udn)
    Dmsitelist.append(Dm)
    Imsitelist.append(Im)
    print math.degrees(Dm),math.degrees(Im)
    N= len(coresinsitelist)
    print N
    print R
    if N==1:
        k=N/(N-R)
        print 'Only one core for'+sites[si]+' Approximations of Fisher statistics will not work properly'
        print 'Continueing on with an approximation of k. Error ellipses are not representative of actual error'
    else:
        k = (N-1)/(N-R) #I had i here, but I think it should be something else 
    a95 = 140/math.sqrt(k*N)# changed an i out here too
    a95r = math.radians(a95)
    print k, a95
    #s =81/math.sqrt(k)
    colatr = math.atan2(2,math.tan(Im))
    foo = math.sin(sitelatr)*math.cos(colatr)
    bar = math.cos(sitelatr)*math.sin(colatr)*math.cos(Dm)
    polelatr = math.asin(foo+bar)
    beta = math.asin(math.sin(colatr)*math.sin(Dm)/math.cos(polelatr))
    if math.cos(colatr)>math.sin(polelatr)*math.sin(beta):
        polelong = sitelong+math.degrees(beta)
    else:
        polelong = sitelong+180-math.degrees(beta)
    dpr = a95r*(1+3*math.cos(colatr)*math.cos(colatr))/2
    dmr = a95r*math.sin(colatr)/math.cos(Im) #poorly named
    dp= math.degrees(dpr)
    dm= math.degrees(dmr)
    dpslist.append(dp)
    dmslist.append(dm)
    latslistr.append(polelatr)
    longslist.append(polelong)
    print 'Site '+sites[si]+' done'