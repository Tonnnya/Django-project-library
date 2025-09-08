from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from library.library.views import health, debug_urls   # імпорт нашого тестового в’ю

def home_redirect(request):
    return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('auth/', include(('authentication.urls', 'authentication'), namespace='authentication')),
    path('_debug_urls/', debug_urls),  # <-- тестова адреса
    path('health/', health),  # перевірка що цей urls.py активний

]

