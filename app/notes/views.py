from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404, QueryDict
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from typing import Union, Dict

from .models import Category, Post
from .forms import AddCategoryForm, AddPostForm, UserRegistrationForm
from .encode import encoding, decoding


@login_required
def index(request: HttpRequest) -> HttpResponse:
    categories: QuerySet = Category.objects.filter(author=request.user)
    context: Dict = {'categories': categories}
    return render(request, 'notes/index.html', context)


@login_required
def category_detail(request: HttpRequest, cat_id: int) -> HttpResponse:
    category: Category = get_object_or_404(Category, pk=cat_id)
    if category.author == request.user:
        context: Dict = {'category': category}
        return render(request, 'notes/category.html', context)
    else:
        return HttpResponseRedirect(reverse('notes:alien'))


@login_required
def category_add(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        add_form: AddCategoryForm = AddCategoryForm(data=request.POST)
        if add_form.is_valid():
            new_category: Category = add_form.save(commit=False)
            new_category.author = request.user
            new_category.save()
            return render(request, 'notes/add_category.html', {'added': True})
    else:
        # add_form = AddCategoryForm()
        # форма прописана в шаблоне. хочу сделать через form.as_p или как-то иначе,
        # но чтобы использовался класс формы
        # но пока не нашел, как использовать при этом красиво бутстрап.
        # поэтому хардкод в шаблоне. Это мне не нравится.
        return render(request, 'notes/add_category.html')  # , {'add_form': add_form})


@login_required
def category_delete(request: HttpRequest, cat_id: int) -> HttpResponseRedirect:
    category: Category = get_object_or_404(Category, pk=cat_id)
    if category.author != request.user:
        return HttpResponseRedirect(reverse('notes:alien'))
    category.delete()
    return HttpResponseRedirect(reverse('notes:index'))


@login_required
def category_rename(request: HttpRequest, cat_id: int) -> Union[HttpResponseRedirect, HttpResponse]:
    category: Category = get_object_or_404(Category, pk=cat_id)
    if category.author != request.user:
        return HttpResponseRedirect(reverse('notes:alien'))
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        return HttpResponseRedirect(reverse('notes:index'))
    else:
        return render(request, 'notes/rename_category.html', {'category': category})


@login_required
def post_detail(request: HttpRequest, post_id: int) -> Union[HttpResponseRedirect, HttpResponse]:
    post: Post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return HttpResponseRedirect(reverse('notes:alien'))
    context: Dict = {'post': post}
    if post.is_secret:
        template: str = 'notes/secure_post.html'
        if request.method == 'POST':
            password: str = request.POST['password']
            salt: bytes = bytes(post.salt)
            token: bytes = bytes(post.secure_body)
            text: str = decoding(salt=salt, password=password, token=token)
            context['text'] = text
    else:
        template: str = 'notes/post.html'
    return render(request, template, context)


@login_required
def post_add(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        add_form: AddPostForm = AddPostForm(data=request.POST)
        if add_form.is_valid():
            new_post: Post = add_form.save(commit=False)
            data: QueryDict = request.POST
            if data.get('is_secret'):
                new_post.salt, new_post.secure_body = encoding(data['body'], data['password'])
                new_post.body = ''
            new_post.author = request.user
            new_post.save()
        return render(request, 'notes/add_post.html', {'post': new_post, 'added': True})
    else:
        categories: QuerySet = request.user.notes_categories.all()
        # add_form = AddPostForm()
        # форма прописана в шаблоне. хочу сделать через form.as_p или как-то иначе,
        # но чтобы использовался класс формы
        # но пока не нашел, как использовать при этом красиво бутстрап.
        # поэтому хардкод в шаблоне. Это мне не нравится.
        return render(request, 'notes/add_post.html', {'categories': categories})  # , {'add_form': add_form})


@login_required
def post_delete(request: HttpRequest, post_id: int) -> HttpResponseRedirect:
    post: Post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return HttpResponseRedirect(reverse('notes:alien'))
    cat_id: int = post.rubric.id
    post.delete()
    return HttpResponseRedirect(reverse('notes:category', kwargs={'cat_id': cat_id}))


@login_required
def post_edit(request: HttpRequest, post_id: int) -> Union[HttpResponseRedirect, HttpResponse]:
    post: Post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return HttpResponseRedirect(reverse('notes:alien'))
    if post.is_secret:
        return secret_post_edit(request, post.id)
    else:
        if request.method == 'POST':
            edit_form: AddPostForm = AddPostForm(data=request.POST)
            if edit_form.is_valid():
                data: QueryDict = request.POST
                post.title = data.get('title')
                post.body = data.get('body')
                if data.get('is_secret'):
                    post.salt, post.secure_body = encoding(data['body'], data['password'])
                    post.body = ''
                    post.is_secret = True
                post.author = request.user
                post.save()
            return render(request, 'notes/edit_post.html', {'post': post, 'saved': True})
        else:
            categories: QuerySet = request.user.notes_categories.all()
            context: Dict = {'post': post, 'categories': categories}
            return render(request, 'notes/edit_post.html', context)


@login_required
def secret_post_edit(request: HttpRequest, post_id: int) -> Union[HttpResponseRedirect, HttpResponse]:
    post: Post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return HttpResponseRedirect(reverse('notes:alien'))
    if request.method == 'POST':
        password: str = request.POST['password']
        salt: bytes = bytes(post.salt)
        token: bytes = bytes(post.secure_body)
        text: str = decoding(salt=salt, password=password, token=token)
        if text == 'Error. Wrong password':
            return render(request, 'notes/edit_secret_post.html', {'post': post, 'error': True})
        post.body = text
        post.is_secret = False
        post.save()
        return HttpResponseRedirect(reverse('notes:post_edit', kwargs={'post_id': post.id}))
    else:
        return render(request, 'notes/edit_secret_post.html', {'post': post})


def alien_post(request: HttpRequest) -> HttpResponse:
    return render(request, 'notes/alien.html')


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form: UserRegistrationForm = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})
