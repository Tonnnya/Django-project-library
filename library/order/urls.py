from django.urls import path
from . import views

urlpatterns = [
    path("all_orders/", views.all_orders_view, name="all_orders"),
    path("my_orders/", views.my_orders_view, name="my_orders"),
    path("create/<int:book_id>/", views.create_order_view, name="create_order"),
    path("close/<int:order_id>/", views.close_order_view, name="close_order"),
]