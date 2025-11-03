from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=150, default='No title')
    author = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_likes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user} {self.book} ({self.like})'