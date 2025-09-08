from django.http import HttpResponse
from django.urls import get_resolver

def health(request):
    return HttpResponse("OK")

def debug_urls(request):
    routes = []
    for p in get_resolver().url_patterns:
        try:
            routes.append(p.pattern._route)  # Django 3/4
        except AttributeError:
            routes.append(str(p.pattern))
    return HttpResponse("<br>".join(routes))



from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')