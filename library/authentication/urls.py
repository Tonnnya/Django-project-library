from django.urls import path
from . import views, user_views

urlpatterns = [
    path('registration_form/', views.registration_view, name='registration_form'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('librarian-account/', views.librarian_account_view, name='librarian_account'),
    path('visitor-account/', views.visitor_account_view, name='visitor_account'),

    path('users/', user_views.all_users_view, name='all_users'),
    path('users/<int:user_id>/', user_views.user_detail_view, name='user_detail'),

    path('register/', views.registration_view, name='register'),
]