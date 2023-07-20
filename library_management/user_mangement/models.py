from django.contrib.auth.models import User
from management_book.models import Book_list
from django.db import models

class BookWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    book = models.ForeignKey(Book_list, on_delete=models.CASCADE, blank = True)


    def __str__(self):
        return f"Wishlist for {self.user.username}"