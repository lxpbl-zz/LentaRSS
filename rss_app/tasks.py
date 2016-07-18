from LentaRSS.celery import app
from rss_app.models import Category, Article

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Q
from django.conf import settings

import pdfkit
import feedparser
from dateutil.parser import parse

from io import BytesIO
from datetime import datetime
import pytz


@app.task(ignore_result=True)
def rss_import():
    d = feedparser.parse('https://lenta.ru/rss/news')
    for entry in d.entries:
        category, _ = Category.objects.get_or_create(name=entry.category)

        _, _ = Article.objects.get_or_create(guid=entry.guid, defaults={
            'title': entry.title,
            'desc': entry.description,
            'pubdate': parse(entry.published),
            'category': category
        })


@app.task(ignore_result=True)
def gen_and_send_pdf(form_data):
    # Should be user-specific timezone, but TIME_ZONE setting for now
    tz = pytz.timezone(settings.TIME_ZONE)
    dt_beg = datetime.combine(form_data['date_beg'], datetime.min.time()).replace(tzinfo=tz)
    dt_end = datetime.combine(form_data['date_end'], datetime.max.time()).replace(tzinfo=tz)
    arts = Article.objects.filter(Q(category__id__in=form_data['cats']) &
                                  Q(pubdate__gte=dt_beg) &
                                  Q(pubdate__lte=dt_end)).order_by('-pubdate')
    cats = Category.objects.filter(id__in=form_data['cats'])
    html = render_to_string('lenta_feed.html', {'arts': arts})
    pdf = pdfkit.from_string(html, False)
    result = BytesIO(pdf)
    email = EmailMessage(
        'Новости с lenta.ru (%s - %s)' % (form_data['date_beg'], form_data['date_end']),
        'Запрошенные категории: %s' % ''.join(('\n' + x.name for x in cats)),
        settings.EMAIL_HOST_USER,
        [form_data['email']]
    )
    email.attach('feed.pdf', result.getvalue(), 'application/pdf')
    email.send()
