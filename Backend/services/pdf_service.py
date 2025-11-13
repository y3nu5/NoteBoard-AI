from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def export_pdf(text):
    file_path = "output.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50
    for line in text.split('\n'):
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    return os.path.abspath(file_path)
