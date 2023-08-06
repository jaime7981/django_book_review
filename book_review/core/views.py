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
