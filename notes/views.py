from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Category
from .forms import AddCategoryForm


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
        add_form = AddCategoryForm()
        return render(request, 'notes/add_category.html', {'add_form': add_form})
