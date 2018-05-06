from django.forms import ModelForm
from .models import Book, Author, Tag, Chapter

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'tags']

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ['name', 'link']

class CountForm(ModelForm):
    class Meta:
        model = Book
        fields = ['count']