from rest_framework import serializers
from api_v2.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.name")

    class Meta:
        model = Book
        fields = "__all__"
