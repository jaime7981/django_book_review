from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField()
    publish_date = models.DateField()

    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE
    )


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    description = models.TextField()

    country = models.ForeignKey(
        'Country',
        on_delete=models.SET_NULL,
        null=True
    )


class Country(models.Model):
    name = models.CharField(max_length=100)


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField()
    upvotes = models.IntegerField()
    date = models.DateField()

    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE
    )


class Sales(models.Model):
    date = models.DateField()
    amount = models.IntegerField()

    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE
    )
