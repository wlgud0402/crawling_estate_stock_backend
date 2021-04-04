from rest_framework import serializers, routers, viewsets
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'content', 'created_at',)
        # fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'text', 'created_at', 'comments',)
        # related_name='comments'


class PostOnlySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'nickname', 'text', 'created_at',)
