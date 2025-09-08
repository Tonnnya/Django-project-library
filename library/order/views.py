from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta

from .models import Order
from book.models import Book

@login_required
def all_orders_view(request):
    if request.user.role != 1:
        raise PermissionDenied
    orders = Order.objects.all()
    return render(request, "order/all_orders.html", {"orders": orders})

@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "order/my_orders.html", {"orders": orders})

@login_required
def create_order_view(request, book_id):
    if request.user.role != 0:
        raise PermissionDenied

    book = get_object_or_404(Book, id = book_id)

    plated_end_at = timezone.now().date() + timedelta(days=14)
    order = Order.create(user=request.user, book=book, plated_end_at=plated_end_at)
    return redirect("my_orders")

@login_required
def close_order_view(request, order_id):
    if request.user.role != 1:
        raise PermissionDenied

    order = get_object_or_404(Order, id=order_id)

    if order.end_at is None:
        order.update(end_at=now())
        messages.success(request, f"Order {order.id} closed successfully.")
    else:
        messages.info(request, f"Order {order.id} is already closed.")

    return redirect("all_orders")

