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
