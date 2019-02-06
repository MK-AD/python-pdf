# python .\pdf_class.py invoice_green
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import sys
import os.path

from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

from reportlab.pdfbase.pdfmetrics import stringWidth

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib import pagesizes
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

from reportlab.platypus import Paragraph, Frame, KeepInFrame


class PdfClass:
    def __init__(self, inputJson=None, logo_url=ImageReader('https://www.google.com/images/srpr/logo11w.png')):
        self.inputJson = inputJson
        self.logo_url = logo_url
        self.today_time = str(datetime.now())[:-15]

    def generate_document(self):
        self.template = self.inputJson.get('template', None)

        if self.template is None:
            return "The template is mandatory"
        elif not os.path.isfile('./ressources/templates/' + self.template + ".pdf"):
            return "The template doesn't exists"

        self.first_name = self.inputJson.get('first_name', '')
        self.last_name = self.inputJson.get('last_name', '')
        self.customer_street = self.inputJson.get('customer_street', '')
        self.customer_zip = self.inputJson.get('customer_zip', '')
        self.customer_phone = self.inputJson.get('customer_phone', '')
        self.items = self.inputJson.get('items', '')

        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=A4)

        can.setFont('Courier', 10, leading=None)


        self.template_content_chooser(self.template, can, self.items)

        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open('./ressources/templates/' + self.template + ".pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open('./ressources/output/output.pdf', "wb")
        output.write(outputStream)
        outputStream.close()

        return self.today_time

    def template_content_chooser(self, template, can, items):
        if template in ('invoice_green', 'invoice_blue'):
            self.template_invoice(can, items)
        if template in ('urkunde_stars'):
            self.template_urkunde(can)

        return

    def template_invoice(self, can, items=None):
        width = 0
        height = 0
        (width, height) = pagesizes.A4

        can.drawImage(self.logo_url, 75, 750, width=150, height=50, mask='auto')
        can.drawString(435, 622, "Hr. Heinrich")
        can.drawString(120, 681, self.first_name + ' ' + self.last_name)
        can.drawString(120, 658, self.customer_street)
        can.drawString(120, 635, self.customer_zip)
        can.drawString(120, 612, self.customer_phone)
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
        width = 0
        height = 0
        (width, height) = pagesizes.landscape(A4)

        # Position / Rolle
        can.setFont('Helvetica', 32, leading=None)
        can.drawCentredString(width / 2, 340, "Projektleiter")

        # Empfänger
        can.setFont('Courier', 20, leading=None)
        can.drawCentredString(width / 2, 255, self.first_name)

        # Herausgeber
        can.setFont('Courier', 20, leading=None)
        can.drawCentredString(width / 2, 195, "Frau Magdeburg")
