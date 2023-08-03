from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField()
    publish_date = models.DateField()

    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    description = models.TextField()

    country = models.ForeignKey(
        'Country',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField()
    upvotes = models.IntegerField()
    date = models.DateField()

    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.book.name}: {self.text}'


class Sales(models.Model):
    date = models.DateField()
    amount = models.IntegerField()

    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.book.name
