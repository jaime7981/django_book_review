from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from django.urls import reverse_lazy
from core.models import Author, Book, Country, Review, Sales
import math
from django.views.generic.edit import UpdateView, CreateView

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
                        PAGINATION_SIZE * (pagination_number): PAGINATION_SIZE * (pagination_number + 1)
                    ]
                else:
                    search_books = search_books[
                        PAGINATION_SIZE * (pagination_number - 1): PAGINATION_SIZE * (pagination_number)
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


class CreateAuthorView(CreateView):
    model = Author
    template_name = 'core/author_form.html'
    fields = ['name', 'birth_date', 'country', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('authors/_core_author_detail', kwargs={'pk': self.object.pk})


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
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('authors/_core_author_detail', kwargs={'pk': self.object.pk})


class CreateBookView(CreateView):
    model = Book
    template_name = 'core/book_form.html'
    fields = ['name', 'summary', 'publish_date', 'author']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('books/_core_book_detail', kwargs={'pk': self.object.pk})


class UpdateBookView(UpdateView):
    model = Book
    template_name = 'core/book_form.html'
    fields = ['name', 'summary', 'publish_date', 'author']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'].publish_date = context['book'].publish_date.strftime('%Y-%m-%d')
        context['authors'] = Author.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('books/_core_book_detail', kwargs={'pk': self.object.pk})


class CreateReviewView(CreateView):
    model = Review
    template_name = 'core/review_form.html'
    fields = ['text', 'rating', 'upvotes', 'date', 'book']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('reviews/_core_review_detail', kwargs={'pk': self.object.pk})


class UpdateReviewView(UpdateView):
    model = Review
    template_name = 'core/review_form.html'
    fields = ['text', 'rating', 'upvotes', 'date', 'book']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'].date = context['review'].date.strftime('%Y-%m-%d')
        context['books'] = Book.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('reviews/_core_review_detail', kwargs={'pk': self.object.pk})


class CreateSaleView(CreateView):
    model = Sales
    template_name = 'core/sales_form.html'
    fields = ['date', 'amount', 'book']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('sales/_core_sales_detail', kwargs={'pk': self.object.pk})


class UpdateSaleView(UpdateView):
    model = Sales
    template_name = 'core/sales_form.html'
    fields = ['date', 'amount', 'book']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context.keys())
        context['sales'].date = context['sales'].date.strftime('%Y-%m-%d')
        context['books'] = Book.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('sales/_core_sales_detail', kwargs={'pk': self.object.pk})
