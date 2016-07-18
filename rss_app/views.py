from django.shortcuts import render
from django.http import HttpResponse
from rss_app.tasks import gen_and_send_pdf
from rss_app.forms import GetNewsForm


def index(request):
    if request.method == 'GET':
        if request.is_ajax():
            form = GetNewsForm(request.GET)
            if form.is_valid():
                gen_and_send_pdf.delay(form.cleaned_data)
                return HttpResponse('OK')
            else:
                return HttpResponse(form.errors.as_json())
        return render(request, 'index.html', {'form': GetNewsForm()})
