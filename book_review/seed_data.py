import os
import django
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
    for country_number in range(20):
        country, created = Country.objects.get_or_create(
            name=fake.country()
        )
        #new_country.save()
    print('countries created')

def create_authors():
    for author_number in range(50):
        Author.objects.create(
            name=fake.name(),
            birth_date=fake.date(),
            description=fake.text(),
            country=foreign_key(Country)
        )

def seed_data():
    print("Seeding data...")
    create_countries()

if __name__ == '__main__':
    seed_data()