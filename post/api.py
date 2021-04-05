from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, PostOnlySerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.paginator import Paginator
import jwt
import math
from django.http import JsonResponse
from user.models import User

one_page_board = 15


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
        page_count = math.ceil(len(queryset)/one_page_board)
        page_count = [i+1 for i in range(page_count)]
        now_page = self.request.query_params.get('page', 1)  # 현재 페이지
        # page_size = self.request.query_params.get('page_size', 2)  # 한 페이지당

        paginator = Paginator(queryset, one_page_board)
        serializer = PostOnlySerializer(paginator.page(
            now_page), many=True, context={'request': request})
        return Response({"boards": serializer.data, "page_count": page_count})

    def post(self, request, format=None):
        try:
            encoded_jwt = request.data.get("token")
            title = request.data.get('title')
            text = request.data.get('text')
            user_token = jwt.decode(
                encoded_jwt, "secret", algorithms=["HS256"])
            user = User.objects.get(id=user_token.get('id'))
            post = Post(user=user, title=title, text=text)
            post.save()
            return JsonResponse({"msg": "게시글이 작성되었습니다."})
        except:
            return JsonResponse({"msg": "게시글 작성은 로그인이 필요합니다."})


class PostDetailAPI(APIView):
    # 게시글 조회
    def get(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # 게시글 수정
    def put(self, request, pk):
        try:
            encoded_jwt = request.data.get("token")
            user_token = jwt.decode(
                encoded_jwt, "secret", algorithms=["HS256"])
            user = User.objects.get(id=user_token.get('id'))
            post = Post.objects.get(pk=pk)

            if post.user.id == user.id:
                post.title = request.data.get('title')
                post.text = request.data.get('text')
                post.save()
                return JsonResponse({"msg": "글이 수정되었습니다."})
            else:
                return JsonResponse({"msg": "권한이 없습니다."})
        except:
            return JsonResponse({"msg": "권한이 없습니다."})
    # 삭제

    def post(self, request, pk):
        try:
            encoded_jwt = request.data.get("token")
            user_token = jwt.decode(
                encoded_jwt, "secret", algorithms=["HS256"])
            user = User.objects.get(id=user_token.get('id'))
            post = Post.objects.get(pk=request.data.get("post_id"))
            if post.user.id == user.id:
                post.delete()
                return JsonResponse({"msg": "글이 삭제되었습니다.."})
            else:
                return JsonResponse({"msg": "권한이 없습니다."})
        except:
            return JsonResponse({"msg": "권한이 없습니다."})


class CommentAPI(APIView):
    def post(self, request):
        try:
            post_id = request.data.get("board_id")
            post = Post.objects.get(id=post_id)
            encoded_jwt = request.data.get("token")
            content = request.data.get("content")
            user_token = jwt.decode(
                encoded_jwt, "secret", algorithms=["HS256"])
            user = User.objects.get(id=user_token.get('id'))
            comment = Comment(user=user, post=post, content=content)
            comment.save()
            return Response({"msg": "댓글이 등록되었습니다."})
        except:
            return Response({"msg": "에러가 발생했습니다. 로그인을 다시 진행해 주세요."})


class CommentDeleteAPI(APIView):
    def post(self, request, format=None):
        try:
            encoded_jwt = request.data.get("token")
            user_token = jwt.decode(
                encoded_jwt, "secret", algorithms=["HS256"])
            user = User.objects.get(id=user_token.get('id'))
            comment_id = request.data.get("comment_id")
            comment = Comment.objects.get(id=comment_id)

            if user.id == comment.user.id:
                comment.delete()
                return JsonResponse({"msg": "댓글이 삭제 되었습니다."})
            else:
                return JsonResponse({"msg": "권한이 없습니다. 로그인을 다시 진행해주세요."})
        except:
            return JsonResponse({"msg": "권한이 없습니다. 로그인을 다시 진행해주세요."})
