from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import title

from .models import Book
from django.contrib.auth.decorators import login_required

from authentication.user_views import librarian_required
from author.models import Author

from django.contrib import messages

@login_required
def books_list_view(request):
    books = Book.objects.all()

    search_query = request.GET.get("q")
    if search_query:
        books = books.filter(name=search_query)

    author_id = request.GET.get("author")
    if author_id:
        books = books.filter(author_id=author_id)

    return render(request, "book/books_list.html", {"books": books})

@login_required
def book_detail_view(request, book_id):
    """Show single book"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book/book_detail.html", {"book": book})

@login_required
def books_by_user_view(request, user_id):
    if request.user.role != 1:
        raise PermissionDenied
    books = Book.objects.filter(user_id=user_id)
    return render(request, "book/books_by_user.html", {"books": books, "user_id": user_id})

@librarian_required
def add_book_view(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            count = request.POST.get("count", 10)
            author_id = request.POST.get("authors")

            if not name:
                messages.error(request, "Book name is required.")
                return render(request, "books/book_form.html", {
                    'author': Author.objects.all().order_by('surname', 'name'),
                    'form_data': {
                        'name': name,
                        'description': description,
                        'count': count
                    }
                })

            book = Book.objects.create(
                name=name,
                description=description,
                count=10
            )

            author = get_object_or_404(Author, id=author_id)
            book.authors.add(author)

            messages.success(request, f"Book '{book.name}' created successfully.")
            return redirect("book_detail", book_id=book.id)

        except ValueError as e:
            messages.error(request, f'Invalid data: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error adding book: {str(e)}')

    author = Author.objects.all().order_by('name')
    context = {'author': author}
    return render(request, "books/book_form.html", context)


@librarian_required
def user_books_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    current_orders = []
    all_orders = []

    context = {'target_user': target_user,
               'current_orders': current_orders,
               'all_orders': all_orders,
               'current_order_count': len(current_orders),
               'complete_order_count': 0,
               'total_order_count': len(all_orders),
               }
    return render(request, "books/user_librarian_books.html", context)
