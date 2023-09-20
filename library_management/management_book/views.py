from .forms import BookSearchForm
from .models import Book_list, BorrowedBook
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from random import sample
from django.contrib import messages
from django.contrib.auth import get_user_model
import random

def random_book(request):
    random_book = Book_list.objects.order_by('?').first()
    return {'random_book': random_book}

def base(request):
    books = Book_list.objects.all()

    # Ensure the sample size does not exceed the total number of books
    num_books_to_show = min(6, len(books))  # Adjust the maximum number of books to show as desired

    if num_books_to_show > 0:
        # Select a random subset of books
        random_books = sample(list(books), num_books_to_show)
    else:
        random_books = []

    return render(request, 'base.html', {'books': random_books})


def book_catalog(request):
    books = Book_list.objects.all()
    return render(request, 'all_books.html', {'books': books})

def book_search(request):
    form = BookSearchForm(request.GET or None)
    books = []

    if form.is_valid():
        search_option = form.cleaned_data['search_option']
        search_query = form.cleaned_data['search_query']

        # Perform the search based on the selected search option and query
        if search_option == 'title':
            books = Book_list.objects.filter(title__icontains=search_query).all()
        elif search_option == 'author':
            books = Book_list.objects.filter(author__icontains=search_query).all()
        elif search_option == 'genre':
            books = Book_list.objects.filter(genre__icontains=search_query).all()
        elif search_option == 'isbn':
            books = Book_list.objects.filter(isbn__icontains=search_query).all()

    return render(request, 'search_books.html', {'form': form, 'books': books})


    if form.is_valid():
        title = form.cleaned_data['title']
        books = Book_list.objects.filter(title__icontains=title)

    return render(request, 'book_management/search.html', {'form': form, 'books': books})

def book_reservation(request, book_id):
    if not book_id:
        return redirect('book_catalog')
    book = get_object_or_404(Book_list, isbn=book_id)


    if not book.availability:
        return redirect('book_catalog')  # Replace 'book_catalog' with the appropriate URL name

    book.availability = False
    book.save()

    # Implement the reservation notification functionality

    return redirect('book_catalog')  # Replace 'book_catalog' with the appropriate URL name
 

