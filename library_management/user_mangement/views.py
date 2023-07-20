from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, ModifiedLoginForm, ReturnBookForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from management_book.models import Book_list, BorrowedBook
from django.contrib import messages
from .models import BookWishlist
from datetime import datetime, timedelta



def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            confirm_password = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            if password != confirm_password:
                form.add_error('confirm_password', "Passwords do not match.")
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                return redirect('user_login')  # Replace 'login' with the URL name for your login view
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = ModifiedLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
                # Redirect to the desired page
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = ModifiedLoginForm(request)
    
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('base')
    return render(request, 'logout.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def my_account(request):
    user = request.user
    return render(request, 'my_account.html', {'user':user})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('user_login:password_change_done')
    success_message = "Your password has been changed successfully."
    
    
@login_required
def add_to_wishlist(request, book_isbn):
    book = get_object_or_404(Book_list, isbn=book_isbn)
    user = request.user

    if book.wishlist.filter(id=user.id).exists():
        # Book already in wishlist, handle accordingly (e.g., show a message)
        messages.warning(request, 'This book is already in your wishlist.')
        pass
    else:
        book.wishlist.add(user)
        messages.warning(request, "You successfully add this book in your wishlist.")
        # Book added to wishlist, handle accordingly (e.g., show a success message)

    return redirect('book_catalog')

@login_required
def remove_from_wishlist(request, book_isbn):
    book = get_object_or_404(Book_list, isbn=book_isbn)

    # Remove the book from the user's wishlist
    if book.wishlist.filter(id=request.user.id).exists():
        book.wishlist.remove(request.user)

    return redirect('wishlist')


@login_required
def wishlist(request):
    # Retrieve the user's wishlist books
    wishlist_books = Book_list.objects.filter(wishlist=request.user)
    
    context = {
        'wishlist_books': wishlist_books
    }
    
    return render(request, 'wishlists.html', context)



@login_required
def borrow_book(request, book_isbn):
    book = get_object_or_404(Book_list, isbn=book_isbn)
    if book.quantity<1:
        book.availability = -1
    else:
        book.avalibility = 1
    # Check if the user has any existing borrowed books
    if BorrowedBook.objects.filter(user=request.user).exists():
        messages.warning(request, "You have already borrowed a book. Please return it before borrowing another book.")
        return redirect('book_catalog')
    if book.quantity > 0:
        # Calculate the due date (e.g., 7 days from the current date)
        due_date = datetime.now().date() + timedelta(days=7)
        borrowed_book = BorrowedBook(user=request.user, book=book, due_date=due_date)
        borrowed_book.save()
        book.quantity -= 1
        book.save()
        messages.success(request, f"You have successfully borrowed '{book.title}'.")
        return redirect('book_catalog')
        if book.quantity <1:
            book.availability = False
        
    else:
        messages.warning(request, f"The book '{book.title}' is currently unavailable.")
        return redirect('book_catalog')
    
@login_required
def borrowed_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    return render(request, 'borrowed_books.html', {'borrowed_books': borrowed_books})
 
    


def return_book(request, borrowed_book_id):
    borrowed_books = BorrowedBook.objects.filter(book__isbn=borrowed_book_id)

    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            return_date = form.cleaned_data['return_date']
            for borrowed_book in borrowed_books:
                borrowed_book.return_date = return_date
                # Don't save the borrowed_book, just delete it from the database
                borrowed_book.delete()

                # Update the book's availability status to True
                book = borrowed_book.book
                book.quantity += 1
                book.save()
                book.availability = True

                # Perform any additional operations related to returning a book,
                # such as calculating fine amount.

            return redirect('book_catalog')  # Replace with the URL name for your book catalog view
    else:
        form = ReturnBookForm()

    return render(request, 'return_book.html', {'form': form, 'borrowed_books': borrowed_books})


@login_required
def total_fine_amount(request):
    if request.user.is_authenticated:
        borrowed_books = BorrowedBook.objects.filter(user=request.user)
        total_fine = sum(book.fine_amount for book in borrowed_books)
        return render(request, 'fine_details.html', {'total_fine': total_fine})
    else:
        return render(request, 'fine_details.html', {'total_fine': 0})



