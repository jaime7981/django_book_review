from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from core.models import Author, Book


# Create your views here.
def main(request):
    return render(request, 'main.html')


def authorsInfo(request):
    # A table that shows authors, number of published books, average score
    # and total sales. This table should have a sort and filter for each
    # column.

    authors = Author.objects.annotate(
        books_count=Count('book'),
        avg_score=Avg('book__review__rating'),
        total_sales=Sum('book__sales__amount')
    )

    return render(request, 'authors_info.html', {'authors_info': authors})


def booksTop10(request):
    # A table that shows the top 10 rated books of all time, with their most
    # popular highest and lowest rated review.
    top_books = Book.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')[:10]

    for book in top_books:
        book.rating = book.avg_rating
        book.best_review = book.review_set.order_by('-rating', '-upvotes').first()
        book.worst_review = book.review_set.order_by('rating', '-upvotes').first()

    context = {
        'top_books': top_books
    }
    return render(request, 'books_top_10.html', context)

def booksTopSelling(request):

    top_selling_books = Book.objects.annotate(total_sales=Sum('sales__amount')).order_by('-total_sales')[:50]

    for book in top_selling_books:
        book.total_sales = book.total_sales
        book.author_sales = getAuthorTotalSalesByBook(book)
        book.is_book_top_5 = isBookTop5SellingOnPublicationYear(book)


    return render(request, 'books_top_50_selling.html', context={'top_selling_books':top_selling_books})

def getAuthorTotalSalesByBook(book):
    author = book.author
    total_sales = 0

    for book in author.book_set.all():
        total_sales += book.sales_set.all().aggregate(Sum('amount'))['amount__sum']

    return total_sales

def isBookTop5SellingOnPublicationYear(book):
    publication_year = book.publish_date
    top_5_selling_books = Book.objects.annotate(total_sales=Sum('sales__amount')).order_by('-total_sales')[:5]

    for book in top_5_selling_books:
        if book.publish_date == publication_year:
            return True

    return False


def search(request, search_query=''):
    # A search box that allows you to search for books by title, author,
    # publisher, genre, and year of publication.
    search_books = Book.objects.none()
    if request.method == 'POST':
        search_query = request.POST.get('search_query')

        if search_query != '':
            search_books = Book.objects.filter(summary__icontains=search_query)

    return render(request, 'search.html', context={'search_books': search_books, 'search_query': search_query})
