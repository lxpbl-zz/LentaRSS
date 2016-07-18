from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)


class Article(models.Model):
    guid = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    desc = models.CharField(max_length=256)
    pubdate = models.DateTimeField()
    category = models.ForeignKey(Category)
