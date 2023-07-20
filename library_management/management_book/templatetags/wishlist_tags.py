from django import template
from management_book.models import Book_list


register = template.Library()

@register.filter
def in_wishlist(book, user):
    return book.wishlist.filter(id=user.id).exists()
