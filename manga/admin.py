from django.contrib import admin
from .models import Author, Tag, Chapter, Book

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Chapter)
admin.site.register(Book)
