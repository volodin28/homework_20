import json
from datetime import datetime

from django.http import JsonResponse
from django.views import View

from .models import Book, Author


class BookList(View):
    def get(self, request):
        books = Book.objects.all()
        data = [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author.name,
                "genre": book.genre,
                'publication_date': book.publication_date
            }
            for book in books
        ]
        return JsonResponse(data, safe=False, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid json"}, status=400)
        title = data.get("title")
        author_check = data.get('author')
        genre = data.get("genre")
        publication_date = data.get("publication_date")

        if not title:
            return JsonResponse({"error": "no title provided"}, status=400)
        if not author_check:
            return JsonResponse({"error": "no author provided"}, status=400)
        if not genre:
            return JsonResponse({"error": "no genre provided"}, status=400)
        if not publication_date:
            return JsonResponse({"error": "no publication date provided"}, status=400)

        try:
            author = Author.objects.get(name=author_check)
        except Author.DoesNotExist:
            author = Author.objects.create(name=author_check)

        try:
            publication_date = datetime.strptime(publication_date, "%Y-%m-%d")
        except ValueError:
            return JsonResponse(
                {"error": "Date format is not correct. Use YYYY-MM-DD format."}, status=400
            )

        book = Book.objects.create(
            title=title, author=author, genre=genre, publication_date=publication_date.date()
        )
        data = {
            "id": book.id,
            "title": book.title,
            "author": author.name,
            "genre": book.genre,
            "publication_date": book.publication_date,
        }
        return JsonResponse(data, safe=False, status=201)


class BookID(View):
    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "ID is not found"}, status=404)
        data = {
                "id": book.id,
                "title": book.title,
                "author": book.author.name,
                "genre": book.genre,
                'publication_date': book.publication_date
            }
        return JsonResponse(data, safe=False, status=200)

    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "ID is not found"}, status=404)

        book.delete()
        return JsonResponse({"success": "The book has been deleted"}, status=200)

    def put(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "ID is not found"}, status=404)
        try:
            data = json.loads(request.body)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid json"}, status=400)

        title = data.get("title")
        author_check = data.get("author")
        genre = data.get("genre")
        publication_date = data.get("publication_date")

        if not (title or author_check or genre or publication_date):
            return JsonResponse({"error": "Data is empty"}, status=400)

        if title:
            book.title = title
        if author_check:
            try:
                Author.objects.get(name=author_check)
            except Author.DoesNotExist:
                author = Author.objects.create(name=author_check)
                book.author_id = Author.objects.get(name=author)
        if genre:
            book.genre = genre
        if publication_date:
            book.publication_date = publication_date

        book.save()

        data = {
            "id": book.id,
            "title": book.title,
            "author": book.author.name,
            "genre": book.genre,
            "publication_date": book.publication_date,
        }
        return JsonResponse(data, safe=False, status=200)


class AuthorList(View):
    def get(self, request):
        authors = Author.objects.all()
        data = [
            {
                "id": author.id,
                "name": author.name,
            }
            for author in authors
        ]
        return JsonResponse(data, safe=False, status=200)


class AuthorID(View):
    def get(self, request, id):
        try:
            author = Author.objects.get(id=id)
        except Author.DoesNotExist:
            return JsonResponse({"error": "ID is not found"}, status=404)

        data = {"id": author.id, "name": author.name}
        return JsonResponse(data, safe=False, status=200)
