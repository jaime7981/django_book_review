import os
import django

# Set the DJANGO_SETTINGS_MODULE to your project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_review.settings')

# Configure Django settings
django.setup()

def seed_data():
    print("Seeding data...")

if __name__ == '__main__':
    seed_data()