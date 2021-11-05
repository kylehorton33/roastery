import io
from datetime import datetime

import qrcode
from django.http import FileResponse
from django.http.response import Http404
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from roastery.coffee.models import Bean, Roast


def make_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def generate_bean_label(request):

    bean_id = request.POST.get("bean_id")
    size = request.POST.get("size")
    width, height = float(size.split("x")[0]), float(size.split("x")[1])

    try:
        bean = Bean.objects.get(id=bean_id)
    except Bean.DoesNotExist:
        raise Http404("Bean does not exist")

    buffer = io.BytesIO()

    pagesize = (width * inch, height * inch)  # label for dymo printer

    c = canvas.Canvas(buffer, pagesize=pagesize)

    c.setFont("Helvetica", 12)

    data = bean.get_label_data()
    now = datetime.now()
    label_timestamp = now.strftime("%a %d %b %Y %H:%M:%S UTC")
    filename = now.strftime("Label-%Y%m%d_%H%M%S")

    img = make_qr_code(data["url"])

    c.drawString(0.2 * inch, 1.6 * inch, f"Name: {data['name']}")
    c.drawString(0.2 * inch, 1.3 * inch, f"Origin: {data['origin']}")
    c.drawInlineImage(img, 2.4 * inch, 0.5 * inch, 1.3 * inch, 1.3 * inch)
    c.setFont("Helvetica", 8)
    c.drawString(0.2 * inch, 0.2 * inch, f"Label Generated: {label_timestamp}")

    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f"{filename}.pdf")


def generate_roast_label(request):

    roast_id = request.POST.get("roast_id")
    size = request.POST.get("size")
    width, height = float(size.split("x")[0]), float(size.split("x")[1])

    try:
        roast = Roast.objects.get(id=roast_id)
    except Roast.DoesNotExist:
        raise Http404("Roast does not exist")

    buffer = io.BytesIO()

    pagesize = (width * inch, height * inch)  # label for dymo printer

    c = canvas.Canvas(buffer, pagesize=pagesize)

    c.setFont("Helvetica", 12)

    data = roast.get_label_data()
    now = datetime.now()
    label_timestamp = now.strftime("%a %d %b %Y %H:%M:%S UTC")
    filename = now.strftime("Label-%Y%m%d_%H%M%S")

    img = make_qr_code(data["url"])

    c.drawString(0.2 * inch, 1.6 * inch, f"Name: {data['name']}")
    c.drawString(0.2 * inch, 1.4 * inch, f"Origin: {data['origin']}")
    c.drawString(0.2 * inch, 1.2 * inch, f"Roast: {data['roast']}")
    c.drawString(0.2 * inch, 0.8 * inch, f"Roasted On: {data['roast_date']}")
    c.drawInlineImage(img, 2.4 * inch, 0.5 * inch, 1.3 * inch, 1.3 * inch)
    c.setFont("Helvetica", 8)
    c.drawString(0.2 * inch, 0.2 * inch, f"Label Generated: {label_timestamp}")

    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f"{filename}.pdf")
