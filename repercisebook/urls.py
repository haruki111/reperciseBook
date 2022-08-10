from re import template
from django.urls import path
from . import views
from django.views.generic import TemplateView, CreateView, ListView, View

app_name = 'repercisebook'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('create/', views.BookCreateView.as_view(), name='create_book'),
    path('detail/<int:pk>/',
         views.BookDetailView.as_view(), name='detail_book'),
    path('detail/section/<int:pk>/',
         views.SectionDetailView.as_view(), name='detail_section'),
    path('delete/<int:pk>/', views.BookDeleteView.as_view(), name='delete_book'),
    path('delete/section/<int:pk>/',
         views.SectionDeleteView.as_view(), name='delete_section'),
    path('delete/problem/<int:pk>/',
         views.ProblemDeleteView.as_view(), name='delete_problem'),
    path('get_book_list/', views.get_book_list, name='get_book_list'),
    path('get_detail_book/<int:pk>/',
         views.get_detail_book, name='get_detail_book'),
    path('get_detail_section/<int:pk>',
         views.get_detail_section, name='get_detail_section'),
    path('create/section/<int:pk>',
         views.SectionCreateView.as_view(), name='create_section'),
    path('create/problem/<int:pk>',
         views.ProblemCreateView.as_view(), name='create_problem')
]
