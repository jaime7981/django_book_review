import os
import django
import random
from datetime import datetime
from faker import Faker

# Set the DJANGO_SETTINGS_MODULE to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_review.settings")

# Configure Django settings
django.setup()
from core.models import Book, Author, Country, Review, Sales  # noqa


# Set Faker
fake = Faker()


def delete_data():
    for country in Country.objects.all():
        country.delete()

    for author in Author.objects.all():
        author.delete()

    for book in Book.objects.all():
        book.delete()

    for review in Review.objects.all():
        review.delete()

    for sales in Sales.objects.all():
        sales.delete()

    print("data deleted")


def create_countries():
    for country_number in range(21):
        country, created = Country.objects.get_or_create(name=fake.country())
    print("countries created")


def create_authors():
    countries = Country.objects.all()
    for author_number in range(51):
        author = Author.objects.create(
            name=fake.name(),
            birth_date=fake.date(),
            description=fake.text(),
            country=random.choice(countries),
        )
        author.save()
        create_books_by_authors(author)


def create_books_by_authors(author):
    for book_number in range(10):
        book = Book.objects.create(
            name=fake.sentence(),
            summary=fake.text(),
            publish_date=fake.date(),
            author=author,
        )
        book.save()
        create_reviews_by_books(book)
        create_sales_by_books(book)


def create_reviews_by_books(book):
    for review_number in range(random.randint(4, 10)):
        review = Review.objects.create(
            text=fake.text(),
            rating=random.randint(1, 5),
            upvotes=random.randint(1, 100),
            date=fake.date(),
            book=book,
        )
        review.save()


def create_sales_by_books(book):
    for sales_year in range(2015, 2023):
        sales = Sales.objects.create(
            date=datetime(sales_year, random.randint(1, 12), random.randint(1, 28)),
            amount=random.randint(100, 1000),
            book=book,
        )
        sales.save()


def seed_data():
    print("Seeding data...")
    delete_data()
    create_countries()
    create_authors()
    print('authors created')
    print('books created')
    print('reviews created')
    print('sales created')


if __name__ == "__main__":
    seed_data()
