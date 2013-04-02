import pylab
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
def stereoplot(strike,dip,filename):    
    #Here is the stereonet plotting section
    
    bigr = 1.2
    phid = pylab.arange(2,90,2)    # Angular range for
    phir = phid*pylab.pi/180
    omegad = 90 - phid 
    omegar = pylab.pi/2-phir
    
    # Set up for plotting great circles with centers along
    # positive x-axis
    
    x1 = bigr* pylab.tan(phir)
    y1 = pylab.zeros(pylab.size(x1))
    r1 =  bigr/pylab.cos(phir)
    theta1ad = (180-80)*pylab.ones(pylab.size(x1))
    theta1ar = theta1ad*pylab.pi/180
    theta1bd = (180+80)*pylab.ones(pylab.size(x1))
    theta1br = theta1bd*pylab.pi/180
    
    # Set up for plotting great circles 
    # with centers along the negative x-axis
    x2 = -1*x1
    y2 = y1
    r2 = r1
    theta2ad = -80*pylab.ones(pylab.size(x2))
    theta2ar = theta2ad*pylab.pi/180
    theta2bd =  80*pylab.ones(pylab.size(x2))
    theta2br = theta2bd*pylab.pi/180
    
    
    # Set up for plotting small circles
    # with centers along the positive y-axis
    y3 = bigr/pylab.sin(omegar)
    x3 = pylab.zeros(pylab.size(y3))
    r3 =  bigr/pylab.tan(omegar)
    theta3ad = 3*90-omegad
    theta3ar = 3*pylab.pi/2-omegar
    theta3bd = 3*90+omegad
    theta3br = 3*pylab.pi/2+omegar
    
    # Set up for plotting small circles
    # with centers along the negative y-axis
    y4 = -1*y3
    x4 = x3
    r4 =  r3
    
    theta4ad = 90-omegad
    theta4ar = pylab.pi/2-omegar
    theta4bd = 90+omegad
    theta4br = pylab.pi/2+omegar
    
    
    # Group all x, y, r, and theta information for great cricles 
    phi = pylab.append(phid, phid,0)
    x = pylab.append(x1,x2,0)
    y = pylab.append(y1, y2,0)
    r = pylab.append(r1, r2)
    
    thetaad = pylab.append(theta1ad, theta2ad,0)
    thetaar = pylab.append(theta1ar, theta2ar,0)
    thetabd =pylab.append(theta1bd, theta2bd,0)
    thetabr =pylab.append(theta1br, theta2br,0)
    
    # Plot portions of all great circles that lie inside the
    # primitive circle, with thick lines (1 pt.) at 10 degree increments
    
    for i in range(0,len(x)):
        thd = pylab.arange(thetaad[i],thetabd[i]+1,1)
        thr = pylab.arange(thetaar[i],thetabr[i]+pylab.pi/180,pylab.pi/180)
        xunit = x[i] + r[i]*pylab.cos(pylab.radians(thd))
        yunit = y[i] + r[i]*pylab.sin(pylab.radians(thd))
        #p = pylab.plot(xunit,yunit,'b',lw=.5) #commented out to remove small verticle lines
        pylab.hold(True)   
    
    
    # Now "blank out" the portions of the great circle cyclographic traces 
    # within 10 degrees of the poles of the primitive circle.
    rr =  bigr/pylab.tan(80*pylab.pi/180)
    ang1 = pylab.arange(0,pylab.pi+pylab.pi/180,pylab.pi/180)
    xx = pylab.zeros(pylab.size(ang1)) + rr*pylab.cos(ang1)
    yy = bigr/pylab.cos(10*pylab.pi/180)*pylab.ones(pylab.size(ang1)) - rr*pylab.sin(ang1)
    p = pylab.fill(xx,yy,'w')
    yy = -bigr/pylab.cos(10*pylab.pi/180)*pylab.ones(pylab.size(ang1)) + rr*pylab.sin(ang1)
    p = pylab.fill(xx,yy,'w')
    
    for i in range(1,len(x)):
        thd = pylab.arange(thetaad[i],thetabd[i]+1,1)
        thr = pylab.arange(thetaar[i],thetabr[i]+pylab.pi/180,pylab.pi/180)
        xunit = x[i] + r[i]*pylab.cos(pylab.radians(thd))
        yunit = y[i] + r[i]*pylab.sin(pylab.radians(thd))
        
        if pylab.mod(phi[i],10) == 0:
            p = pylab.plot(xunit,yunit,'b',lw=1)
            angg = thetaad[i]
        pylab.hold(True)
    
    
    # Now "blank out" the portions of the great circle cyclographic traces 
    # within 2 degrees of the poles of the primitive circle.
    rr =  bigr/pylab.tan(88*pylab.pi/180)
    ang1 = pylab.arange(0,pylab.pi+pylab.pi/180,pylab.pi/180)
    xx = pylab.zeros(pylab.size(ang1)) + rr*pylab.cos(ang1)
    yy = bigr/pylab.cos(2*pylab.pi/180)*pylab.ones(pylab.size(ang1)) - rr*pylab.sin(ang1)
    
    p = pylab.fill(xx,yy,'w')
    yy = -bigr/pylab.cos(2*pylab.pi/180)*pylab.ones(pylab.size(ang1)) + rr*pylab.sin(ang1)
    p = pylab.fill(xx,yy,'w')
    
    
    # Group all x, y, r, and theta information for small circles
    phi = pylab.append(phid, phid,0)
    x = pylab.append(x3,x4,0)
    y = pylab.append(y3, y4,0)
    r = pylab.append(r3, r4)
    
    thetaad = pylab.append(theta3ad, theta4ad,0)
    thetaar = pylab.append(theta3ar, theta4ar,0)
    thetabd =pylab.append(theta3bd, theta4bd,0)
    thetabr =pylab.append(theta3br, theta4br,0)
    
    # Plot primitive circle
    thd = pylab.arange(0,360+1,1)
    thr = pylab.arange(0,2*pylab.pi+pylab.pi/180,pylab.pi/180)
    xunit = bigr*pylab.cos(pylab.radians(thd))
    
    yunit = bigr*pylab.sin(pylab.radians(thd))
    p = pylab.plot(xunit,yunit)
    pylab.hold(True)
        
    # Plot portions of all small circles that lie inside the
    # primitive circle, with thick lines (1 pt.) at 10 degree increments
    
    for i in range(0,len(x)):
        thd = pylab.arange(thetaad[i],thetabd[i]+1,1)
        thr = pylab.arange(thetaar[i],thetabr[i]+pylab.pi/180,pylab.pi/180)
        xunit = x[i] + r[i]*pylab.cos(pylab.radians(thd))
        yunit = y[i] + r[i]*pylab.sin(pylab.radians(thd))
        blug = pylab.mod(thetaad[i],10)
        if pylab.mod(phi[i],10) == 0:
            p = pylab.plot(xunit,yunit,'b',lw=1)
            angg = thetaad[i]
        #else: #Commented out to remove the small horizontal lines
            #p = pylab.plot(xunit,yunit,'b',lw=0.5)
        pylab.hold(True)
    
    # Draw thick north-south and east-west diameters
    xunit = [-bigr,bigr]
    yunit = [0,0]
    p = pylab.plot(xunit,yunit,'b',lw=1)
    pylab.hold(True)
    xunit = [0,0]
    yunit = [-bigr,bigr]
    p = pylab.plot(xunit,yunit,'b',lw=1)
    pylab.hold(True)
    
    '''
    This is the plotting part'''
    
   
    trend1 = strike
    plunge1 = pylab.absolute(dip)
    #num = leng(lines1(:,1));
    trendr1 = [foo*pylab.pi/180 for foo in trend1]
    
    plunger1 = [foo*pylab.pi/180 for foo in plunge1]
    rho1 = [bigr*pylab.tan(pylab.pi/4 - ((foo)/2)) for foo in plunger1]
        # polarb plots ccl from 3:00, so convert to cl from 12:00
    #pylab.polar(pylab.pi/2-trendr1,rho1,'o')
    pylab.plot(9000,90000,'o',markerfacecolor="b",label='Positive Dip')
    pylab.plot(9000,90000,'o',markerfacecolor="w",label='Negative Dip')      
    pylab.legend(loc=1) 
    for n in range(0,len(strike)):
        if dip[n] > 0:
            pylab.plot(rho1[n]*pylab.cos(pylab.pi/2-trendr1[n]),rho1[n]*pylab.sin(pylab.pi/2-trendr1[n]),'o',markerfacecolor="b",label='Positive Dip')
        else:
            pylab.plot(rho1[n]*pylab.cos(pylab.pi/2-trendr1[n]),rho1[n]*pylab.sin(pylab.pi/2-trendr1[n]),'o',markerfacecolor="w",label='Negative Dip')
         
    '''above is self'''
    pylab.axis([-bigr, bigr, -bigr, bigr])