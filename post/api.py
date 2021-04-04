from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, PostOnlySerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.paginator import Paginator


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_number'
    max_page_size = 3


class PostListAPI(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination


class PostAPI(APIView):
    def get(self, request, format=None):
        queryset = Post.objects.all()
        now_page = self.request.query_params.get('page', 1)  # 현재 페이지
        # page_size = self.request.query_params.get('page_size', 2)  # 한 페이지당

        paginator = Paginator(queryset, 3)
        serializer = PostOnlySerializer(paginator.page(
            now_page), many=True, context={'request': request})
        return Response(serializer.data)
    # def get(self, request, format=None):
    #     queryset = Post.objects.all()
    #     serializer = PostOnlySerializer(queryset, many=True)
    #     return Response(serializer.data)


class PostDetailAPI(APIView):
    # 게시글 조회
    def get(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # 게시글 수정
    def put(self, request, pk, format=None):
        pass

    def delete(self, request, pk, format=None):
        pass
