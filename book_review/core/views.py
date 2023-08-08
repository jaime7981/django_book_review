from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from core.models import Author, Book, Country
import math
from django.views.generic.edit import UpdateView

PAGINATION_SIZE = 10


# Create your views here.
def main(request):
    return render(request, "main.html")


def authorsInfo(request):
    # A table that shows authors, number of published books, average score
    # and total sales. This table should have a sort and filter for each
    # column.

    authors = Author.objects.annotate(
        books_count=Count("book"),
        avg_score=Avg("book__review__rating"),
        total_sales=Sum("book__sales__amount"),
    )

    return render(request, "authors_info.html", {"authors_info": authors})


def booksTop10(request):
    # A table that shows the top 10 rated books of all time, with their most
    # popular highest and lowest rated review.
    top_books = Book.objects.annotate(avg_rating=Avg("review__rating")).order_by(
        "-avg_rating"
    )[:10]

    for book in top_books:
        book.rating = book.avg_rating
        book.best_review = book.review_set.order_by("-rating", "-upvotes").first()
        book.worst_review = book.review_set.order_by("rating", "-upvotes").first()

    context = {"top_books": top_books}
    return render(request, "books_top_10.html", context)


def booksTopSelling(request):
    top_selling_books = Book.objects.annotate(
        total_sales=Sum("sales__amount")
    ).order_by("-total_sales")[:50]

    for book in top_selling_books:
        book.total_sales = book.total_sales
        book.author_sales = getAuthorTotalSalesByBook(book)
        book.is_book_top_5 = isBookTop5SellingOnPublicationYear(book)

    return render(
        request,
        "books_top_50_selling.html",
        context={"top_selling_books": top_selling_books},
    )


def getAuthorTotalSalesByBook(book):
    author = book.author
    total_sales = 0

    for book in author.book_set.all():
        author_total_sales = book.sales_set.all().aggregate(Sum("amount"))[
            "amount__sum"
        ]
        if author_total_sales is not None:
            total_sales += author_total_sales

    return total_sales


def isBookTop5SellingOnPublicationYear(book):
    publication_year = book.publish_date
    top_5_selling_books = Book.objects.annotate(
        total_sales=Sum("sales__amount")
    ).order_by("-total_sales")[:5]

    for book in top_5_selling_books:
        if book.publish_date == publication_year:
            return True

    return False


def search(request, pagination_number=1, search_query=""):
    # A search box that allows you to search for books by title, author,
    # publisher, genre, and year of publication.
    search_books = Book.objects.none()
    max_pagination_number = 0

    if request.method == "POST":
        search_query = request.POST.get("search_query")

        if search_query != "":
            words = search_query.split(" ")
            for word in words:
                search_books = search_books | Book.objects.filter(
                    summary__icontains=word
                )

            max_pagination_number = math.ceil(search_books.count() / PAGINATION_SIZE)

            if search_books.count() > PAGINATION_SIZE:
                search_books = search_books[:PAGINATION_SIZE]

    elif request.method == "GET":
        search_query = request.GET.get("search_query")

        if search_query != "" and search_query is not None:
            words = search_query.split(" ")
            for word in words:
                search_books = search_books | Book.objects.filter(
                    summary__icontains=word
                )

            if pagination_number < 1:
                pagination_number = 1

            max_pagination_number = math.ceil(search_books.count() / PAGINATION_SIZE)

            if pagination_number == 1:
                search_books = search_books[:PAGINATION_SIZE]

            elif search_books.count() > PAGINATION_SIZE * pagination_number:
                if search_books.count() < PAGINATION_SIZE * (pagination_number + 1):
                    search_books = search_books[
                        PAGINATION_SIZE * (pagination_number - 1): PAGINATION_SIZE * pagination_number
                    ]

            elif search_books.count() < PAGINATION_SIZE * pagination_number:
                search_books = search_books[PAGINATION_SIZE * (pagination_number - 1):]

    return render(
        request,
        "search.html",
        context={
            "search_books": search_books,
            "search_query": search_query,
            "pagination_number": pagination_number,
            "max_pagination_number": list(range(1, max_pagination_number + 1)),
        },
    )


def createAuthor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        country = request.POST.get('country')
        description = request.POST.get('description')
        birth_date = request.POST.get('birth_date')

        author = Author.objects.create(
            name=name,
            birth_date=birth_date,
            country_id=country,
            description=description
        )
        return render(request, "core/author_detail.html", {"author": author})
    else:
        countries = Country.objects.all()
        return render(request, "core/author_form.html", {"countries": countries})


class UpdateAuthorView(UpdateView):
    model = Author
    template_name = 'core/author_form.html'
    fields = ['name', 'country', 'description', 'birth_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'].birth_date = context['author'].birth_date.strftime('%Y-%m-%d')
        context['countries'] = Country.objects.all()
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return render(self.request, 'core/author_detail.html', {'author': self.object})


def createBook(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        summary = request.POST.get('summary')
        publish_date = request.POST.get('publish_date')
        country = request.POST.get('country')

        book = Book.objects.create(
            name=name,
            summary=summary,
            publish_date=publish_date,
            country_id=country
        )

        return render(request, "core/book_detail.html", {"book": book})
    else:
        authors = Author.objects.all()
        return render(request, "core/book_form.html", {"authors": authors})


class UpdateBookView(UpdateView):
    model = Book
    template_name = 'core/book_form.html'
    fields = ['name', 'summary', 'publish_date', 'author']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'].publish_date = context['book'].publish_date.strftime('%Y-%m-%d')
        context['authors'] = Author.objects.all()
        print(context['authors'])
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return render(self.request, 'core/book_detail.html', {'book': self.object})
