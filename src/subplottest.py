import pylab
import addimagepage
'''
fig=pylab.plot()

pylab.subplot(2,2,1)
pylab.plot([1,2,3],[3,1,2])


pylab.plot([2,2,3],[3,1,2])
pylab.subplot(2,2,2)

pylab.plot([1,2,3],[3,1,2])
pylab.subplot(2,2,3)


pylab.subplot(2,2,4)
pylab.plot([1,2,3],[3,1,2])
pylab.show()

pylab.plot([1,2,3],[3,1,2])
pylab.subplot(2,2,4)

pylab.savefig('pdfpage.png')
addimagepage.addimagepage('pdfpage', '.png')'''
import stereoplot
stereoplot.stereoplot([0], [0], 'bork.png')
pylab.show()
