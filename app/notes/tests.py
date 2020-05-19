from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from .models import Category, Post
from .forms import UserRegistrationForm


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user')
        Category.objects.create(name='Work', author=user)

    def test_category_name_is_field_name(self):
        cat = Category.objects.get(name='Work')
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


class IndexPageTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', email='email@email.com', password='12345')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('notes:index'))
        self.assertRedirects(response, '/login/?next=/')

    def test_login(self):
        self.client.post('/login/', {'username': 'testuser1', 'password': '12345'})
        response = self.client.get('')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logged_in_uses_correct_template(self):
        self.client.post('/login/', {'username': 'testuser1', 'password': '12345'})
        response = self.client.get('')

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/index.html')


class CategoryDetailPageTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', email='email@email.com', password='12345')
        test_user1.save()

    def test_user_try_to_open_alien_category(self):
        self.client.post('/login/', {'username': 'testuser1', 'password': '12345'})
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()
        cat = Category.objects.create(name='category', author=test_user2)
        response = self.client.get('/category/%s/' % cat.id)
        self.assertRedirects(response, '/alien/')


class SecretPostPageTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser', email='email@email.com', password='12345')
        test_user.save()

    def test_user_try_to_open_secret_note(self):
        self.client.post('/login/', {'username': 'testuser', 'password': '12345'})
        response = self.client.get('')
        cat = Category.objects.create(name='category', author=response.context['user'])
        note = Post.objects.create(title='title', rubric=cat, author=response.context['user'], is_secret=True)
        response = self.client.get('/post/%s/' % note.id)

        self.assertTemplateUsed(response, 'notes/secure_post.html')


class SecretPostAddPageTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser', email='email@email.com', password='12345')
        test_user.save()

    def test_create_secret_post_and_get_text_back(self):
        self.client.post('/login/', {'username': 'testuser', 'password': '12345'})
        response = self.client.get('')
        cat = Category.objects.create(name='category', author=response.context['user'])
        self.client.get('notes:post_add')
        self.client.post(reverse('notes:post_add'), {
                                                    'title': 'title',
                                                    'body': 'secret text',
                                                    'rubric': cat.id,
                                                    'is_secret': True,
                                                    'password': 'password'})
        note = Post.objects.get(title='title')
        response = self.client.post('/post/%s/' % note.id, {'password': 'password'})
        self.assertEqual(response.context['text'], 'secret text')
