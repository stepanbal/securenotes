from django.test import TestCase
from django.contrib.auth.models import User

from .models import Category, Post


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user')
        Category.objects.create(name='Work', author=user)

    def test_category_name_is_field_name(self):
        cat = Category.objects.get(id=1)
        expected_object_name = cat.name
        self.assertEquals(expected_object_name, str(cat))


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user')
        cat = Category.objects.create(name='Work', author=user)
        Post.objects.create(title='Work 1', author=user, rubric=cat)

    def test_post_name_is_field_title(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.title
        self.assertEquals(expected_object_name, str(post))
