from django.urls import path
from . import views


app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:cat_id>', views.category_detail, name='category'),
    path('category/add/', views.category_add, name='category_add'),
]
