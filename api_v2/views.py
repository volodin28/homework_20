from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookList(APIView):
    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        data = Book.objects.all()
        serializer = BookSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            author_check = serializer.validated_data.get("author")
            try:
                author = Author.objects.get(name=author_check["name"])
            except Author.DoesNotExist:
                author = Author.objects.create(name=author_check["name"])
            book = serializer.save(author=author)

            data = {
                "id": book.id,
                "title": book.title,
                "author": author.name,
                "genre": book.genre,
                "publication_date": book.publication_date,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookID(APIView):
    def check_id(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, id):
        book_identified = self.check_id(id)
        serializer = BookSerializer(book_identified)
        return Response(serializer.data)

    def put(self, request, id):
        book_identified = self.check_id(id)
        serializer = BookSerializer(book_identified, data=request.data, partial=True)
        if serializer.is_valid():
            author_check = serializer.validated_data.get("author")
            if author_check:
                try:
                    author = Author.objects.get(name=author_check["name"])
                except Author.DoesNotExist:
                    author = Author.objects.create(name=author_check["name"])
                serializer.validated_data["author"] = author

            book = serializer.save()
            data = {
                "id": book.id,
                "title": book.title,
                "author": book.author.name,
                "genre": book.genre,
                "publication_date": book.publication_date,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        book_identified = self.check_id(id)
        book_identified.delete()
        return JsonResponse({"success": "The book has been deleted"}, status=200)


class AuthorList(APIView):
    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        data = Author.objects.all()
        serializer = AuthorSerializer(data, many=True)
        return Response(serializer.data)


class AuthorID(APIView):
    def get(self, request, id):
        try:
            author = Author.objects.get(id=id)
        except Author.DoesNotExist:
            raise Http404
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
