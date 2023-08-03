from django.shortcuts import render
from models import Book, Author, Country, Review, Sales

# Create your views here.
def main(request):
    authors = Author.objects.all()
    return render(request, 'main.html', context={'authors': authors})