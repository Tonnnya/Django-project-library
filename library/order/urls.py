from django.urls import path
from . import views

urlpatterns = [
    # User order management
    path('my/', views.my_orders_view, name='my_orders'),
    path('create/<int:book_id>/', views.create_order_view, name='create_order'),
    path('return/<int:order_id>/', views.return_book_view, name='return_book'),
    path('detail/<int:order_id>/', views.order_detail_view, name='order_detail'),

    # Librarian order management
    path('all/', views.all_orders_view, name='all_orders'),
    path('close/<int:order_id>/', views.close_order_view, name='close_order'),
    path('user/<int:user_id>/', views.user_orders_view, name='user_orders'),
]