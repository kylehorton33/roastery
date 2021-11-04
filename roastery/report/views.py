import io
from datetime import datetime

import qrcode
from django.http import FileResponse
from django.http.response import Http404
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from roastery.coffee.models import Bean


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

    try:
        bean = Bean.objects.get(id=bean_id)
    except Bean.DoesNotExist:
        raise Http404("Bean does not exist")

    buffer = io.BytesIO()

    pagesize = (4 * inch, 2.12 * inch)  # label for dymo printer

    c = canvas.Canvas(buffer, pagesize=pagesize)

    text_object = c.beginText()
    text_object.setTextOrigin(0.2 * inch, 1.6 * inch)
    text_object.setFont("Helvetica", 12)

    data = bean.get_label_data()

    lines = [
        f"Name: {data['name']}",
        f"Origin: {data['origin']}",
    ]

    img = make_qr_code(data["url"])

    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)

    c.drawInlineImage(img, 2.4 * inch, 0.5 * inch, 1.3 * inch, 1.3 * inch)

    c.showPage()
    c.save()

    now = datetime.now().strftime("%Y%m%d-%H%M%S")

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f"{now}.pdf")
