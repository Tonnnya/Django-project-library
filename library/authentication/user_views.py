from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import CustomUser


def librarian_required(view_function):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_librarian():
            messages.error(request, 'You are not a librarian.')
            return redirect('visitor_account')
        return view_function(request, *args, **kwargs)

    return wrapper


@login_required
def all_users_view(request):
    users = CustomUser.objects.all().order_by('-created_at')

    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    if role_filter and role_filter.isdigit():
        users = users.filter(role=int(role_filter))

    if status_filter:
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)

    total_users = CustomUser.objects.count()
    total_librarians = CustomUser.objects.filter(role=1).count()
    total_visitors = CustomUser.objects.filter(role=0).count()
    active_users = CustomUser.objects.filter(is_active=True).count()

    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'total_users': total_users,
        'total_librarians': total_librarians,
        'total_visitors': total_visitors,
        'active_users': active_users,
    }
    return render(request, 'authentication/all_users.html', context)


@login_required
def user_detail_view(request, user_id):
    user_to_view = get_object_or_404(CustomUser, id=user_id)

    if not request.user.is_librarian() and request.user.id != user_id:
        messages.error(request, 'You can only view your own account.')
        return redirect('visitor_account')

    context = {
        'user_to_view': user_to_view,
        'is_own_profile': request.user.id == user_id,
        'can_edit': request.user.is_librarian() or request.user.id == user_id,
    }

    return render(request, 'authentication/user_detail.html', context)
