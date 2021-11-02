import io
from datetime import datetime

import qrcode
from django.conf import settings
from django.http import FileResponse
from django.http.response import Http404
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from roastery.coffee.models import Bean


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

    lines = [
        f"Name: {bean.name}",
        f"Origin: {bean.country.name}",
    ]

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    host = f"https://{settings.ALLOWED_HOSTS[0]}"  # this works in production if host is the only/first ALLOWED_HOST
    if settings.DEBUG:
        host = f"http://{settings.ALLOWED_HOSTS[-1]}:8000"  # if running locally, host is development machine
    qr.add_data(f"{host}{bean.get_absolute_url()}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)

    c.drawInlineImage(img, 2.4 * inch, 0.5 * inch, 1.3 * inch, 1.3 * inch)

    c.showPage()
    c.save()

    now = datetime.now().strftime("%Y%m%d-%H%M%S")

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f"{now}.pdf")
