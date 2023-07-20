from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()
class Book_list(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, primary_key=True)
    publication_date = models.DateField()
    genre = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)
    wishlist = models.ManyToManyField(User, related_name='Wishlist', blank=True)
    reserved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='reserved_books'
    )

    def __str__(self):
        return self.title


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book_list, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)