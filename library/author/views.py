from django.shortcuts import render, redirect, get_object_or_404
from .models import Author
from book.models import Book
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def librarian_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.role != 1:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

@librarian_required
def authors_list_view(request):
    authors = Author.objects.all()
    return render(request, "author/authors_list.html", {"authors": authors})

@librarian_required
def create_author_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        patronymic = request.POST.get("patronymic") or None

        author = Author.create(name, surname, patronymic)
        if author:
            return redirect("authors_list")

        else:
            return render(request, "author/create_author.html", {
                "error": "Invalid data for author"
            })

    return render(request, "author/create_author.html")

@librarian_required
def delete_author_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    if author.books.exists():
        messages.error(request, "You cannot delete this author because he is attached to a book.")
        return redirect("authors_list")

    author.delete()
    messages.success(request, "Author deleted successfully.")
    return redirect("authors_list")





