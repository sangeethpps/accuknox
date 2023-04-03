from rest_framework import serializers
from core.models import *


class SocialNetworkSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')

    class Meta:
        model = SocialNetworkUsers
        fields = ['user_id', 'email']
