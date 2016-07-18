# LentaRSS

## Installation & Running

1. Run in root folder: `pip install -r requirements.txt`
2. Choose a celery broker ([RabbitMQ](https://www.rabbitmq.com/) would be a great choice)
3. Install [wkhtmltopdf](http://wkhtmltopdf.org/), as it's needed by PDFKit. Make sure it will be accessible from PDFKit module.
4. Run `celery -A LentaRSS beat`. It will launch a celerybeat, in order to process schedule tasks
5. Run `celery -A LentaRSS worker -l info`
6. Finally, run `python manage.py runserver`

## Email configuring

As this project made for sending PDF to email, you'll need to configure sender email settings. In `settings.py`, there is an example, based on gmail host:

```
# Email (gmail for example)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'username@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

You can simply replace `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` with your needs or use another, non-gmail, host.
