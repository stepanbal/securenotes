from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name: str = models.CharField(max_length=250, blank=False)
    author: str = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='notes_categories')

    def __str__(self: 'Category') -> str:
        return self.name

    class Meta:
        ordering: tuple = ('name',)


class Post(models.Model):
    title: str = models.CharField(max_length=250, blank=False)
    body: str = models.TextField(blank=True)
    secure_body: bytes = models.BinaryField(blank=True)
    created: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)
    rubric: Category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                         related_name='posts')
    author: User = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='notes_posts')
    salt: bytes = models.BinaryField(blank=True)
    is_secret: bool = models.BooleanField(default=True)

    def __str__(self: 'Post') -> str:
        return self.title

    class Meta:
        ordering = ('-created',)
