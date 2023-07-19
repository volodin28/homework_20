from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

from .views import BookList, AuthorList, BookID, AuthorID, RegistrationView

urlpatterns = [
    path("books", csrf_exempt(BookList.as_view()), name="book_list_2"),
    path("books/<int:id>", csrf_exempt(BookID.as_view()), name="book_id_2"),
    path("authors", csrf_exempt(AuthorList.as_view()), name="authors_list_2"),
    path("authors/<int:id>", csrf_exempt(AuthorID.as_view()), name="authors_id_2"),
    path("registration", csrf_exempt(RegistrationView.as_view()), name="registration"),
    path('token', obtain_auth_token, name='get_token_auth')
]
