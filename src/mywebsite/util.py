from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML


def render_to_pdf(template_path, context_dict):
    # Render HTML template
    html_string = render_to_string(template_path, context_dict)

    # Create PDF using WeasyPrint
    pdf_file = HTML(string=html_string).write_pdf()

    # Create HTTP response with PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv.pdf"'
    response.write(pdf_file)

    return response
