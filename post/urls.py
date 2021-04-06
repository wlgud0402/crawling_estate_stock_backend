from django.urls import path, include
from .api import PostAPI, PostDetailAPI, CommentAPI

urlpatterns = [
    path('', PostAPI.as_view(), name='posts_all'),
    path('<int:pk>/', PostDetailAPI.as_view(), name='post_detail'),
    path('comment/', CommentAPI.as_view(), name='comment'),
    path('comment/<int:pk>', CommentAPI.as_view(), name='comment_detail'),
]
