from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser


def registration_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        middle_name = request.POST.get('middle_name', '')
        role = int(request.POST.get('role', 0))

        if not email or not password:
            messages.error(request, 'Email and/or password are required.')
            return render(request, 'authentication/registration_form.html')

        if password != password_confirmation:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/registration_form.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'authentication/registration_form.html')

        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                role=role
            )
            user.is_active = True
            user.save()
            messages.success(request, 'User created successfully. Log in')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')

    return render(request, 'authentication/registration_form.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email and/or password are required.')
            return render(request, 'login.html')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Hello, {user.first_name} {user.last_name} {user.email}! You are now logged in')

            if user.is_librarian():
                return redirect('librarian_account')
            else:
                return redirect('visitor_account')
        else:
            messages.error(request, 'Email and/or password are invalid.')

    return render(request, 'authentication/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_librarian():
        return redirect('librarian_account')
    else:
        return redirect('visitor_account')

@login_required
def librarian_account_view(request):
    if not request.user.is_librarian():
        messages.error(request, 'You are not a librarian.')
        return redirect('visitor_account')

    return render(request, 'authentication/librarian_account.html')

@login_required
def visitor_account_view(request):
    return render(request, 'authentication/visitor_account.html')

