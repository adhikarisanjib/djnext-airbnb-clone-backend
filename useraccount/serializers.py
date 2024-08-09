from rest_framework import serializers

from useraccount.models import CustomUser


class UserAccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'name',
            'avatar_url',
            'is_staff',
            'is_active',
            'date_joined',
        ]
        