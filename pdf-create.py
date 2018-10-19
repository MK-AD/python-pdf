from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import pagesizes
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')

canvas = Canvas('output.pdf', pagesize=pagesizes.A4)
(width, height) = pagesizes.A4

background_img = 'background.png'
canvas.drawImage(background_img, 0, 0, width=width, height=height, mask='auto')

canvas.drawImage(logo, width/4.0, 550, width=300, height=100, mask='auto')

canvas.setFont('Helvetica', 32, leading=None)
canvas.drawCentredString(width/2.0, 700, "Certificate of")

canvas.setFont('Courier', 24, leading=None)
canvas.drawCentredString(width/2.0, 450, "Florian Kröber")

frame1 = Frame(width/15.0, 80, 500, 300, showBoundary=0)

sp = ParagraphStyle('parrafos',
                            alignment=TA_CENTER,
                            fontSize=14,
                            fontName="Helvetica")
content = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
story = [Paragraph(content, sp)]
frame1.addFromList(story, canvas)

canvas.setFont('Helvetica', 12, leading=None)
canvas.drawCentredString(width/2.0, 20, "I was created with python")


canvas.showPage()
canvas.save()