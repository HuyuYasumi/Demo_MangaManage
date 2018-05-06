from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .models import Author, Tag, Book, Chapter
from .forms import BookForm, AuthorForm, TagForm, ChapterForm, CountForm
from . import  getIgnore, app

class IndexView(ListView):
    model = Book
    template_name = 'manga/index.html'
    context_object_name = 'manga_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 1]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number-2) if (page_number-2) > 0 else 0:page_number-1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number-2) if (page_number-2) > 0 else 0:page_number-1]
            right = page_range[page_number:page_number+1]
            if right[-1] < total_pages-1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last
        }
        return data

class DetailView(IndexView):
    model = Chapter
    template_name = 'manga/detail.html'
    context_object_name = 'chapter_list'

    def get_queryset(self):
        books = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        return super(DetailView, self).get_queryset().filter(book=books)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        book = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        countform = CountForm();
        data = {
            'book': book,
            'form': countform,
        }
        context.update(data)
        return context

class AuthorView(IndexView):
    def get_queryset(self):
        au = get_object_or_404(Author, pk=self.kwargs.get('pk'))
        return super(AuthorView, self).get_queryset().filter(author=au)

class TagView(IndexView):
    def get_queryset(self):
        tags = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tags)

def create_manga(request):
    if request.method == 'POST':
        bookform = BookForm(request.POST)
        if bookform.is_valid():
            bookform.save()
            return HttpResponseRedirect('/create_manga/?message=success')
        else:
            return HttpResponseRedirect('/create_manga/?message=false')
    elif request.method == 'GET':
        bookform = BookForm()
        authorform = AuthorForm()
        tagform = TagForm()
        context = {
            'form': bookform,
            'authorform': authorform,
            'tagform': tagform,
        }
        message = request.GET.get('message')
        if message == 'success':
            context['success'] = True
        elif message == 'false':
            context['false'] = True
        elif message == 'author_success':
            context['author_success'] = True
        elif message == 'author_false':
            context['author_false'] = True
        elif message == 'tag_success':
            context['tag_success'] = True
        elif message == 'tag_false':
            context['tag_false'] = True
        return render(request, 'manga/create_manga.html', context)

def create_author(request):
    if request.method == 'POST':
        authorform = AuthorForm(request.POST)
        if authorform.is_valid():
            authorform.save()
            return HttpResponseRedirect('/create_manga/?message=author_success')
        else:
            return HttpResponseRedirect('/create_manga/?message=author_false')
    elif request.method == 'GET':
        return HttpResponseRedirect('/create_manga/')

def create_tag(request):
    if request.method == 'POST':
        tagform = TagForm(request.POST)
        if tagform.is_valid():
            tagform.save()
            return HttpResponseRedirect('/create_manga/?message=tag_success')
        else:
            return HttpResponseRedirect('/create_manga/?message=tag_false')
    elif request.method == 'GET':
        return HttpResponseRedirect('/create_manga/')

def change_count(request):
    pk = request.GET.get('pk')
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        countform = CountForm(request.POST, instance=book)
        if countform.is_valid():
            countform.save()
            return HttpResponseRedirect('/books/'+pk+'/?message=tag_success')
        else:
            return HttpResponseRedirect('/books/'+pk+'/?message=tag_false')
    elif request.method == 'GET':
        return HttpResponseRedirect('/books/'+pk+'/')

def create_chapter(request):
    pk = request.GET.get('pk')
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        method = request.GET.get('method')
        chapterform = ChapterForm(request.POST)
        if chapterform.is_valid():
            chapter = chapterform.save(commit=False)
            chapter.book = book
            url = chapter.link
            if method == 'A':
                try:
                    url_title = getIgnore.getImageUrl(url)
                    chapter.local_link = getIgnore.getimage(url_title[0], url_title[1])
                except Exception as e:
                    print(e)
                    return HttpResponseRedirect('/create_chapter/?pk='+pk+'&message=chapter_false')
            elif method == 'B':
                try:
                    chapter.local_link = app.main(url)
                except Exception as e:
                    print(e)
                    return HttpResponseRedirect('/create_chapter/?pk='+pk+'&message=chapter_false')
            chapter.save()
            return HttpResponseRedirect('/create_chapter/?pk='+pk+'&message=chapter_success')
        else:
            return HttpResponseRedirect('/create_chapter/?pk='+pk+'&message=chapter_false')
    elif request.method == 'GET':
        chapterform = ChapterForm()
        context = {
            'form': chapterform,
            'pk': pk,
        }
        message = request.GET.get('message')
        if message == 'chapter_success':
            context['success'] = True
        elif message == 'chapter_false':
            context['false'] = True
        return render(request, 'manga/create_chapter.html', context)

