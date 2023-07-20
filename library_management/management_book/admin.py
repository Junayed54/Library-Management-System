from django.contrib import admin
from .models import Book_list, BorrowedBook
# Register your models here.
admin.site.register(Book_list)
admin.site.register(BorrowedBook)