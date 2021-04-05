from django.urls import path, include
from .api import PostListAPI, PostAPI, PostDetailAPI, CommentAPI, CommentDeleteAPI

urlpatterns = [
    path('', PostAPI.as_view(), name='posts_all'),
    path('<int:pk>/', PostDetailAPI.as_view(), name='post_detail'),
    path('comment/', CommentAPI.as_view(), name='comment'),
    path('comment/delete/', CommentDeleteAPI.as_view(), name='delete_comment'),
]
