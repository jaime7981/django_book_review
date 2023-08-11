from generic_scaffold import CrudManager
from .models import Book, Author, Country, Review, Sales
from .views import UpdateAuthorView, UpdateBookView, UpdateReviewView, UpdateSaleView


class BookCrudManager(CrudManager):
    model = Book
    prefix = 'books/'
    update_view_class = UpdateBookView


class AuthorCrudManager(CrudManager):
    model = Author
    prefix = 'authors/'
    update_view_class = UpdateAuthorView


class CountryCrudManager(CrudManager):
    model = Country
    prefix = 'countries/'


class ReviewCrudManager(CrudManager):
    model = Review
    prefix = 'reviews/'
    update_view_class = UpdateReviewView


class SalesCrudManager(CrudManager):
    model = Sales
    prefix = 'sales/'
    update_view_class = UpdateSaleView
