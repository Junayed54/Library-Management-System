from django.urls import path
from user_mangement import views
from .views import ChangePasswordView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('my_account/', views.my_account, name = 'my_account'),
    path('password/change/', ChangePasswordView.as_view(), name='password_change'),
    path('wishlist/add/<str:book_isbn>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<str:book_isbn>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('borrow/<str:book_isbn>/', views.borrow_book, name='borrow_book'),
    path('borrowed-books/', views.borrowed_books, name='borrowed_books'),
    path('return-book/<str:borrowed_book_id>/', views.return_book, name='return_book'),
    path('fine/', views.total_fine_amount, name='fine_details'),



]
