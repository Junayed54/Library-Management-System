from django.urls import path
from .import views

urlpatterns = [
    path('', views.base, name='base'),
    path('all_books/', views.all_books, name='all_books'),
    path('search/', views.book_search, name='book_search'),
    path('reservation/<str:book_id>/', views.book_reservation, name='book_reservation'),
]