from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views


app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:cat_id>/', views.category_detail, name='category'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/del/<int:cat_id>/', views.category_delete, name='category_delete'),
    path('category/rename/<int:cat_id>/', views.category_rename, name='category_rename'),
    path('post/<int:post_id>/', views.post_detail, name='post'),
    path('post/add/', views.post_add, name='post_add'),
    path('post/del/<int:post_id>/', views.post_delete, name='post_delete'),
    path('post/edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('post/decode/<int:post_id>/', views.secret_post_edit, name='decode'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('notes:password_change_done')),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
