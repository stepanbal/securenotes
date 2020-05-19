from django.test import TestCase
from django.contrib.auth.models import User

from .models import Category, Post
from .forms import UserRegistrationForm


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


class UserRegistrationFormTest(TestCase):

    def test_clean_password2_match_passwords(self):
        password = '12345678'
        password2 = '12345678'
        form_data = {'username': 'user', 'password': password, 'password2': password2}
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_password2_mismatch_passwords(self):
        password = '12345678'
        password2 = '12345679'
        form_data = {'username': 'user', 'password': password, 'password2': password2}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
