import io
from datetime import datetime

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
    text_object.setTextOrigin(0.2 * inch, 0.2 * inch)
    text_object.setFont("Helvetica", 12)

    lines = [
        f"Name: {bean.name}",
        f"Origin: {bean.country.name}",
    ]

    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)

    c.showPage()
    c.save()

    now = datetime.now().strftime("%Y%m%d-%H%M%S")

    # auto-download behavior is a product of browser settings, not Django app
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f"{now}.pdf")
