
# python .\pdf_class.py invoice_green
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import sys

from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

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
		
		
	def todayy(self):
		packet = io.BytesIO()
		# create a new PDF with Reportlab
		can = canvas.Canvas(packet, pagesize=A4)
		(width, height) = pagesizes.A4
		can.drawImage(self.logo_url, 75, 750, width=150, height=50, mask='auto')
		can.setFont('Courier', 10, leading=None)

		self.template_content_chooser(self.template, can)
		
		self.content_items(can)
		
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
		
	def content_items(self, can):
		items = ["Red-Shirt", "Blue-Shirt", "Green-Shirt"]
		position_x = 530
		
		for item in items:
			can.drawString(75, position_x, str(items.index(item)))
			can.drawString(140, position_x, item)
			position_x = position_x - 23
			
	def template_content_chooser(self, template, can):
		if template in ('invoice_green', 'invoice_blue'):
			self.template_invoice(can)
		return
	
	def template_invoice(self, can):
		can.drawString(435, 622, "Hr. Heinrich")
		can.drawString(120, 681, self.customer_name)
		can.drawString(120, 658, "Nymphenburger Str. 5")
		can.drawString(120, 635, "80335")
		can.drawString(120, 612, "0123 / 456 789 9")
		can.drawString(435, 670, self.today_time)
		can.drawString(435, 645, "A-123")	
		
today_time = PdfClass('invoice_green', ImageReader('https://www.google.com/images/srpr/logo11w.png'), 'Michael K')
print(today_time.todayy())