import os
import django

# Set the DJANGO_SETTINGS_MODULE to your project's settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CleverHubInterface.settings')

# Configure Django settings
django.setup()

from django.contrib.auth.models import User

def seed_data():
    print("Seeding data...")

if __name__ == '__main__':
    seed_data()