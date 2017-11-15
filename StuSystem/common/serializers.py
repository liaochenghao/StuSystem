# coding: utf-8
from rest_framework import serializers
from common.models import FirstLevel, SecondLevel
from source.models import Campus


class CampusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time']


class SecondLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondLevel
        fields = ['id', 'name', 'key']


class FirstLevelSerializer(serializers.ModelSerializer):
    second_levels = SecondLevelSerializer(many=True, read_only=True)

    class Meta:
        model = FirstLevel
        fields = ['id', 'name', 'key', 'second_levels']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data