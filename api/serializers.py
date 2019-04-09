# coding: utf-8

from rest_framework import serializers

from api.models import User, Customer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer for validate user creation or update
    """

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create user and it's profile
        :param validated_data:
        :return:
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Create user and it's profile
        :param validated_data:
        :return:
        """
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for validate Customer creation or update
    """

    class Meta:
        model = Customer
        fields = ('url', 'company_title', 'tax_office', 'tax_number')

    def create(self, validated_data):
        """
        Create company and additional info
        :param validated_data:
        :return:
        """
        validated_data.update({'lead': True})
        customer = Customer(**validated_data)
        customer.save()
        return customer

    def update(self, instance, validated_data):
        """
        Upadate company and it's additional info
        :param validated_data:
        :return:
        """
        instance.lead = validated_data.get('lead', instance.lead)
        instance.save()

        return instance
