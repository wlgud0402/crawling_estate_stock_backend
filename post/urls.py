from django.urls import path, include
from .api import PostListAPI, PostAPI, PostDetailAPI, CommentAPI

urlpatterns = [
    # path('', PostListAPI.as_view(), name='posts'),
    # path('', PostListAPI.as_view(), name='posts'),
    path('', PostAPI.as_view(), name='posts_all'),
    path('<int:pk>/', PostDetailAPI.as_view(), name='post_detail'),

    path('comment/', CommentAPI .as_view(), name='comment'),
]
