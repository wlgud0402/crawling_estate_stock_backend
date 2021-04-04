from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
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
