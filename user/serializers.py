from rest_framework import serializers
from .models import User
from post.models import Post, Comment


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('google_id', 'email', 'nickname', 'created_at',)


class PostInfoSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at',)


class CommentInfoSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    post_id = serializers.IntegerField(source='post.id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'content', 'created_at',)


class UserInfoSerializer(serializers.ModelSerializer):
    comments = CommentInfoSerializer(many=True, read_only=True)
    posts = PostInfoSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = User
        fields = ('email', 'created_at', 'comments', 'posts',)
