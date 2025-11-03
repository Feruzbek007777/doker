from rest_framework import serializers
from .models import Book, Like


class BookSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'likes', 'dislikes']

    def get_likes(self, instance):
        return instance.likes.filter(like=True).count()

    def get_dislikes(self, instance):
        return instance.likes.filter(like=False).count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'book', 'like']
        read_only_fields = ['user']
