from rest_framework import serializers
from .models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('google_id', 'email', 'nickname',)
