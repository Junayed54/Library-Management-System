from django.urls import path
from .import views

urlpatterns = [
    path('', views.base, name='base'),
    path('catalog/', views.book_catalog, name='book_catalog'),
    path('search/', views.book_search, name='book_search'),
    path('reservation/<str:book_id>/', views.book_reservation, name='book_reservation'),
    # path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist')
]