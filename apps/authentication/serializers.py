from rest_framework import serializers

from apps.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user
