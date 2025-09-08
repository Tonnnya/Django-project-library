from django.urls import path
from . import views


urlpatterns = [
    path('authors_list/', views.authors_list_view, name='authors_list'),
    path('create/', views.create_author_view, name='create_author'),
    path('delete_author/<int:author_id>/', views.delete_author_view, name='delete_author')
]