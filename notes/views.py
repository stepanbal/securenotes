from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Category, Post
from .forms import AddCategoryForm, AddPostForm
from .encode import encoding, decoding


def index(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'notes/index.html', context)


def category_detail(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id)
    context = {'category': category}
    return render(request, 'notes/category.html', context)


def category_add(request):
    if request.method == 'POST':
        add_form = AddCategoryForm(data=request.POST)
        if add_form.is_valid():
            new_category = add_form.save(commit=False)
            new_category.author = User.objects.get(pk=1)
            new_category.save()
            return render(request, 'notes/add_category.html', {'added': True})
    else:
        # add_form = AddCategoryForm()
        # форма прописана в шаблоне. хочу сделать через form.as_p или как-то иначе,
        # но чтобы использовался класс формы
        # но пока не нашел, как использовать при этом красиво бутстрап.
        # поэтому хардкод в шаблоне. Это мне не нравится.
        return render(request, 'notes/add_category.html')  # , {'add_form': add_form})


def category_delete(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id)
    category.delete()
    return HttpResponseRedirect(reverse('notes:index'))


def category_rename(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        return HttpResponseRedirect(reverse('notes:index'))
    else:
        return render(request, 'notes/rename_category.html', {'category': category})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    if post.is_secret:
        template = 'notes/secure_post.html'
        if request.method == 'POST':
            password = request.POST['password']
            salt = bytes(post.salt)
            token = bytes(post.secure_body)
            text = decoding(salt=salt, password=password, token=token)
            context['text'] = text
    else:
        template = 'notes/post.html'
    return render(request, template, context)


def post_add(request):
    if request.method == 'POST':
        add_form = AddPostForm(data=request.POST)
        if add_form.is_valid():
            new_post = add_form.save(commit=False)
            data = request.POST
            if data.get('is_secret'):
                new_post.salt, new_post.secure_body = encoding(data['body'], data['password'])
                new_post.body = ''
            new_post.author = User.objects.get(pk=1)
            new_post.save()
        return render(request, 'notes/add_post.html', {'post': new_post, 'added': True})
    else:
        categories = User.objects.get(pk=1).notes_categories.all()
        # add_form = AddPostForm()
        # форма прописана в шаблоне. хочу сделать через form.as_p или как-то иначе,
        # но чтобы использовался класс формы
        # но пока не нашел, как использовать при этом красиво бутстрап.
        # поэтому хардкод в шаблоне. Это мне не нравится.
        return render(request, 'notes/add_post.html', {'categories': categories})  # , {'add_form': add_form})


def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    cat_id = post.rubric.id
    post.delete()
    return HttpResponseRedirect(reverse('notes:category', kwargs={'cat_id': cat_id}))


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.is_secret:
        return secret_post_edit(request, post.id)
    else:
        if request.method == 'POST':
            edit_form = AddPostForm(data=request.POST)
            if edit_form.is_valid():
                data = request.POST
                post.title = data.get('title')
                post.body = data.get('body')
                if data.get('is_secret'):
                    post.salt, post.secure_body = encoding(data['body'], data['password'])
                    post.body = ''
                    post.is_secret = True
                post.author = User.objects.get(pk=1)
                post.save()
            return render(request, 'notes/edit_post.html', {'post': post, 'saved': True})
        else:
            categories = User.objects.get(pk=1).notes_categories.all()
            context = {'post': post, 'categories': categories}
            return render(request, 'notes/edit_post.html', context)


def secret_post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        password = request.POST['password']
        salt = bytes(post.salt)
        token = bytes(post.secure_body)
        text = decoding(salt=salt, password=password, token=token)
        if text == 'Error. Wrong password':
            return render(request, 'notes/edit_secret_post.html', {'post': post, 'error': True})
        post.body = text
        post.is_secret = False
        post.save()
        return HttpResponseRedirect(reverse('notes:post_edit', kwargs={'post_id': post.id}))
    else:
        return render(request, 'notes/edit_secret_post.html', {'post': post})
