from reportlab.pdfgen import canvas

def addimagepage(imagename,extension):
    c = canvas.Canvas(imagename+".pdf")
    c.drawImage(imagename+extension,0,0,width=8.5*72, preserveAspectRatio=True,anchor='n')
    c.save()