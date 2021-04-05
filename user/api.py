from rest_framework.views import APIView
from .models import User
from post.models import Post, Comment
from .serializers import UserSerializer, UserInfoSerializer
from django.http import JsonResponse
from rest_framework.response import Response
import jwt
import json


class UserAPI(APIView):
    def post(self, request, format=None):
        google_id = request.data.get("googleId")
        email = request.data.get("email")
        nickname = email.split("@")[0]

        user, created = User.objects.get_or_create(
            google_id=google_id,
            email=email,
            nickname=nickname)

        # jwt token response
        user_token = jwt.encode(
            {'id': user.id, 'nickname': user.nickname},
            "secret", algorithm="HS256")
        return JsonResponse({
            'user_token': user_token
        })


class UserDeleteAPI(APIView):
    def post(self, request, format=None):
        try:
            encoded_jwt = request.data.get("token")
            user_token = jwt.decode(
                encoded_jwt, "secret", algorithms=["HS256"])
            user = User.objects.get(id=user_token.get('id'))
            user.delete()
            return JsonResponse({"msg": "회원탈퇴가 완료되었습니다."})
        except:
            return JsonResponse({"msg": "권한이 없습니다. 로그인을 다시 진행해주세요."})


class UserInfoAPI(APIView):
    # 내정보 + 내가쓴글 + 내가쓴 댓글
    def post(self, request, format=None):
        encoded_jwt = request.data.get("user_token")
        user_token = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user = User.objects.get(id=user_token.get('id'))
        # print(user.comments.all().values())
        serializer = UserInfoSerializer(user)
        return JsonResponse({
            'userInfos': serializer.data
        })
