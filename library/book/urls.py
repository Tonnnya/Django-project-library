from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.books_list_view, name='books_list'),
    path('detail/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('books_by_user/user/<int:user_id>/', views.books_by_user_view, name='books_by_user'),

    path('add', views.add_book_view, name='add_book'),
    path('users/<int:user_id>/books/', views.user_books_view, name='user_books'),
    path('', views.books_list_view, name='books_list_view'),

]