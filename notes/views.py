from django.shortcuts import render, get_object_or_404
from .models import Category


def index(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'notes/index.html', context)


def category_detail(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id)
    context = {'category': category}
    return render(request, 'notes/category.html', context)
