from ..models import Book, Author, Tag
from django.db.models.aggregates import Count
from django import template

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Book.objects.all().order_by('-create_time')[:num]

@register.simple_tag
def get_author():
    return Author.objects.all()

@register.simple_tag
def get_tags():
    return Tag.objects.all()
