
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="books.index"),
    path('list_books/', views.list_books, name="books.list_books"),
    path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
    path('aboutus/', views.aboutus, name="books.aboutus"),
    path('html5/links/', views.html5_links, name="books.html5_links"),
    path('html5/text/formatting/', views.html5_text_formatting, name="books.html5_text_formatting"),
    path('html5/listing/', views.html5_listing, name="books.html5_listing"),
    path('html5/tables/', views.html5_tables, name="books.html5_tables"),
    path('search', views.search, name="books.search"),

    # lab7 urls
    path('simple/query', views.simple_query, name="books.simple_query"),
    path('complex/query', views.complex_query, name="books.complex_query"),
]
