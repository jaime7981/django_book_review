import os
import django
import random
from faker import factory, Faker
from model_bakery.recipe import Recipe,foreign_key 

# Set the DJANGO_SETTINGS_MODULE to your project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_review.settings')

# Configure Django settings
django.setup()

from books.models import Book, Author, Country, Review, Sales

#Set Faker
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
    
    print('data deleted')

def create_countries():
    for country_number in range(21):
        country, created = Country.objects.get_or_create(
            name=fake.country()
        )
        #new_country.save()
    print('countries created')

def create_authors():
    countries = Country.objects.all()
    for author_number in range(51):
        author = Author.objects.create(
            name=fake.name(),
            birth_date=fake.date(),
            description=fake.text(),
            country=random.choice(countries)
        )
        author.save()

def seed_data():
    print("Seeding data...")
    delete_data()
    create_countries()
    create_authors()

if __name__ == '__main__':
    seed_data()