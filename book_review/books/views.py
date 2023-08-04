from django.shortcuts import render
from .models import Book, Author, Country, Review, Sales

# Create your views here.
def main(request):
    authors = Author.objects.all()
    return render(request, 'main.html', context={'authors': authors})

def crud(request):
    return render(request, 'crud.html')

def author(request, author_id=None):
    if author_id == None:
        authors = Author.objects.all()
        return render(request, 'authors.html', context={'authors': authors})
    else:
        author = Author.objects.get(id=author_id)
        return render(request, 'author.html', context={'author': author})