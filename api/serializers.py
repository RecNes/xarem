# coding: utf-8

from rest_framework import serializers

from api.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer
    """
    class Meta:
        model = UserProfile
        fields = ('title', )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer for validate user creation or update
    """
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create user and it's profile
        :param validated_data:
        :return:
        """
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        """
        Create user and it's profile
        :param validated_data:
        :return:
        """
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.save()

        return instance
