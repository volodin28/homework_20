from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BookList, BookID, AuthorList, AuthorID

urlpatterns = [
    path("books", csrf_exempt(BookList.as_view()), name="book_list"),
    path("books/<int:id>", csrf_exempt(BookID.as_view()), name="book_id"),
    path("authors", csrf_exempt(AuthorList.as_view()), name='authors_list'),
    path("authors/<int:id>", csrf_exempt(AuthorID.as_view()), name="authors_id"),
]