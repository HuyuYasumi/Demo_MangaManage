from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, 'models.DO_NOTHING')
    tags = models.ManyToManyField(Tag, blank=True)
    count = models.CharField(max_length=100, default='0')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_time']

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    book = models.ForeignKey(Book, 'models.DO_NOTHING')
    link = models.CharField(max_length=200)
    local_link = models.CharField(max_length=200)

    def __str__(self):
        return self.link
