# myapp/serializers.py

from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id','title', 'content', 'author', 'created_by', 'created_at', 'is_draft', 'scheduled_time', 'likes', 'users_liked', 'shares', 'comments']
        read_only_fields = ['created_by']
