from rest_framework import serializers, routers, viewsets
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%m-%d %H:%M")
    nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'nickname', 'content', 'created_at',)
        # fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    user_nickname = serializers.CharField(
        source='user.nickname', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user_nickname', 'title',
                  'text', 'created_at', 'comments',)
        # related_name='comments'


class PostOnlySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%m-%d")
    nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'nickname', 'text', 'created_at',)
