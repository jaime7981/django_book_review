from generic_scaffold import CrudManager
from books.models import Book, Author, Country, Review, Sales


class BookCrudManager(CrudManager):
    model = Book
    prefix = 'books'


class AuthorCrudManager(CrudManager):
    model = Author
    prefix = 'authors'


class CountryCrudManager(CrudManager):
    model = Country
    prefix = 'countries'


class ReviewCrudManager(CrudManager):
    model = Review
    prefix = 'reviews'


class SalesCrudManager(CrudManager):
    model = Sales
    prefix = 'sales'
