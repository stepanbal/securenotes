from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=250, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='notes_categories')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


class Post(models.Model):
    title = models.CharField(max_length=250, blank=False)
    body = models.TextField(blank=True)
    secure_body = models.BinaryField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rubric = models.ForeignKey(Category, on_delete=models.CASCADE,
                               related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='notes_posts')
    salt = models.BinaryField(blank=True)
    is_secret = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)
