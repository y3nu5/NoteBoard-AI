# services/pdf_service.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_pdf(text: str, file_path: str = "output.pdf") -> str:
    """
    Membuat file PDF dari teks (simple, line by line).
    Mengembalikan path file.
    """
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    margin_left = 50
    margin_top = 50
    y = height - margin_top
    line_height = 14

    for line in text.split('\n'):
        # split panjang jadi beberapa baris jika perlu (simple wrap)
        if not line:
            y -= line_height
        else:
            # simple wrapping per 90 karakter (bukan ideal tapi cukup)
            max_chars = 90
            while len(line) > max_chars:
                chunk = line[:max_chars]
                c.drawString(margin_left, y, chunk)
                line = line[max_chars:]
                y -= line_height
                if y < margin_top:
                    c.showPage()
                    y = height - margin_top
            # terakhir
            c.drawString(margin_left, y, line)
            y -= line_height

        if y < margin_top:
            c.showPage()
            y = height - margin_top

    c.save()
    return file_path
