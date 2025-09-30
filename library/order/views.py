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
        raise PermissionDenied('Only librarian can view all orders')

    active_orders = Order.get_active_orders().select_related('user', 'book')
    returned_orders = Order.get_returned_orders().select_related('user', 'book')[:50]
    overdue_orders = [order for order in active_orders if order.is_overdue]

    total_active = active_orders.count()
    total_overdue = len(overdue_orders)
    total_returned = returned_orders.count()

    context = {
        'active_orders': active_orders,
        'returned_orders': returned_orders,
        'overdue_orders': overdue_orders,
        'stats': {
            'total_active': total_active,
            'total_overdue': total_overdue,
            'total_returned': total_returned,
        }
    }

    return render(request, 'order/all_orders.html', context)

@login_required
def my_orders_view(request):
    if request.user.role != 0:
        raise PermissionDenied('Only visitors have personal orders')

    active_orders = Order.objects.filter(user=request.user, end_at__isnull=True).select_related('book')
    returned_orders = Order.objects.filter(user=request.user, end_at__isnull=False).select_related('book')

    overdue_count = sum(1 for order in active_orders if order.is_overdue)

    context = {
        'active_orders': active_orders,
        'returned_orders': returned_orders,
        'stats': {
            'active_count': active_orders.count(),
            'returned_count': returned_orders.count(),
            'overdue_count': overdue_count,
        }
    }
    return render(request, "order/my_orders.html", context)

@login_required
def create_order_view(request, book_id):
    if request.user.role != 0:
        raise PermissionDenied('Only visitors can order books')

    book = get_object_or_404(Book, id = book_id)
    if request.method == "POST":
        try:
            plated_end_at = timezone.now().date() + timedelta(days=14)
            order = Order.create(user=request.user, book=book, plated_end_at=plated_end_at)

            if order:
                messages.success(request, f"Successfully ordered '{book.name}'. Due date: {order.plated_end_at.strftime('%m/%d/%Y')}")
                return redirect('my_orders')
            else:
                messages.error(request, "Unable to create order. Book may not be available or you already have an active order for this book.")
                return redirect('book_detail', book_id=book.id)

        except Exception as e:
            messages.error(request, f"Error creating order: {str(e)}")
            return redirect('book_detail', book_id=book.id)

    existing_order = Order.objects.filter(
        user=request.user,
        book=book,
        end_at__isnull=True
    ).first()

    context = {
        'book': book,
        'existing_order': existing_order,
        'due_date': (timezone.now() + timedelta(days=14)).date()
    }

    return render(request, 'order/create_order.html', context)


@login_required
def close_order_view(request, order_id):
    if request.user.role != 1:
        raise PermissionDenied('Only librarian can close orders')

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        if order.end_at is None:
            order.return_book()
            messages.success(request, f"Order #{order.id} for '{order.book.name}' closed successfully. Book returned by {order.user.email}.")
        else:
            messages.info(request, f"Order {order.id} is already closed.")

        return redirect("all_orders")

    context = {'order': order}
    return render(request, 'order/close_order_confirm.html', context)


@login_required
def return_book_view(request, order_id):
    """User requests to return book"""
    if request.user.role != 0:
        raise PermissionDenied("Only visitors can return books")

    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.end_at is not None:
        messages.info(request, "This book has already been returned.")
        return redirect("my_orders")

    if request.method == "POST":
        order.return_book()
        messages.success(request, f"Book '{order.book.name}' returned successfully.")
        return redirect("my_orders")

    context = {'order': order}
    return render(request, "order/return_confirm.html", context)


@login_required
def order_detail_view(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id)

    # Permission check
    if request.user.role == 0:  # Visitor
        if order.user != request.user:
            raise PermissionDenied("You can only view your own orders")
    elif request.user.role != 1:  # Not librarian
        raise PermissionDenied("Access denied")

    context = {
        'order': order,
        'can_return': order.is_active and (request.user.role == 1 or order.user == request.user)
    }

    return render(request, "order/order_detail.html", context)


@login_required
def user_orders_view(request, user_id):
    """View orders for specific user (librarians only)"""
    if request.user.role != 1:
        raise PermissionDenied("Only librarians can view user orders")

    from authentication.models import CustomUser
    user = get_object_or_404(CustomUser, id=user_id)

    active_orders = Order.objects.filter(user=user, end_at__isnull=True).select_related('book')
    returned_orders = Order.objects.filter(user=user, end_at__isnull=False).select_related('book')

    context = {
        'target_user': user,
        'active_orders': active_orders,
        'returned_orders': returned_orders,
        'stats': {
            'active_count': active_orders.count(),
            'returned_count': returned_orders.count(),
            'overdue_count': sum(1 for order in active_orders if order.is_overdue)
        }
    }

    return render(request, "order/user_orders.html", context)
