from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(extra_context={'create_or_login': 'Login'}), name='index'),
    path('create/', views.CreateView.as_view(extra_context={'create_or_login': 'Create a new user'}), name='create'),
    path('user/', views.UserView.as_view(), name='user'),
    path('bookentry/', views.AddBook.as_view(), name='add_book'),
]