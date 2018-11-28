
# python .\pdf_class.py invoice_green
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import sys

from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

from reportlab.pdfbase.pdfmetrics import stringWidth

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import pagesizes
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

from reportlab.platypus import Paragraph, Frame, KeepInFrame

class PdfClass:
	def __init__(self, 
				template = 'Dokument2', 
				logo_url = ImageReader('https://www.google.com/images/srpr/logo11w.png'),
				customer_name = 'Mr. X'):
		self.template = sys.argv[1]
		self.logo_url = logo_url
		self.customer_name = customer_name
		self.today_time = str(datetime.now())[:-15]
		
		
	def generate_document(self):
		packet = io.BytesIO()
		# create a new PDF with Reportlab
		can = canvas.Canvas(packet, pagesize=A4)
		self.width = 0
		self.height = 0
		(self.width, self.height) = pagesizes.A4
		
		can.setFont('Courier', 10, leading=None)

		items = ["Red-Shirt", "Blue-Shirt", "Green-Shirt", "Haha", "Test", "Against", "The Machine"]
		self.template_content_chooser(self.template, can, items)
		
		
		can.save()

		#move to the beginning of the StringIO buffer
		packet.seek(0)
		new_pdf = PdfFileReader(packet)
		# read your existing PDF
		existing_pdf = PdfFileReader(open('templates/' + self.template + ".pdf", "rb"))
		output = PdfFileWriter()
		# add the "watermark" (which is the new pdf) on the existing page
		page = existing_pdf.getPage(0)
		page.mergePage(new_pdf.getPage(0))
		output.addPage(page)
		# finally, write "output" to a real file
		outputStream = open('output/' + self.template + "_output.pdf", "wb")
		output.write(outputStream)
		outputStream.close()
	

		return self.today_time

			
	def template_content_chooser(self, template, can, items):
		if template in ('invoice_green', 'invoice_blue'):
			self.template_invoice(can, items)
		if template in ('urkunde_stars'):
			self.template_urkunde(can)
			
		return
	
	def template_invoice(self, can, items = None):
		can.drawImage(self.logo_url, 75, 750, width=150, height=50, mask='auto')
		can.drawString(435, 622, "Hr. Heinrich")
		can.drawString(120, 681, self.customer_name)
		can.drawString(120, 658, "Nymphenburger Str. 5")
		can.drawString(120, 635, "80335")
		can.drawString(120, 612, "0123 / 456 789 9")
		can.drawString(435, 670, self.today_time)
		can.drawString(435, 645, "A-123")	
		
		if items is not None:
			self.template_invoice_content_items(can, items)
		
	def template_invoice_content_items(self, can, items):
		position_x = 530
		
		for item in items:
			can.drawString(75, position_x, str(items.index(item)))
			can.drawString(140, position_x, item)
			position_x = position_x - 23	
		
	def template_urkunde(self, can):
		# Position / Rolle
		can.setFont('Courier', 30, leading=None)
		pos_text = "Projektleiter"
		pos_text_width = stringWidth(pos_text, 'Courier', 30)
	
		can.drawCentredString(self.width / 2, 340, pos_text)
	
		# Empfänger
		can.setFont('Courier', 20, leading=None)
		can.drawString(self.width/2.0, 255, "Hr. Heinrich")
		
		#Herausgeber
		can.setFont('Courier', 20, leading=None)
		can.drawString(self.width/2.0, 195, "Frau Magdeburg")
		
		
		
gendoc = PdfClass('invoice_green', ImageReader('https://www.google.com/images/srpr/logo11w.png'), 'Michael K')
print(gendoc.generate_document())