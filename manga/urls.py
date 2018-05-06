from django.urls import path
from . import views

app_name = 'manga_url'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index_url'),
    path('create_manga/', views.create_manga, name='create_manga'),
    path('create_author/', views.create_author, name='create_author'),
    path('create_tag/', views.create_tag, name='create_tag'),
    path('change_count/', views.change_count, name='change_count'),
    path('books/<int:pk>/', views.DetailView.as_view(), name='detail_url'),
    path('author/<int:pk>/', views.AuthorView.as_view(), name='author_url'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag_url'),
    path('create_chapter/', views.create_chapter, name='create_chapter'),
]
