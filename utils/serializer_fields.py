# coding: utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class VerboseChoiceField(serializers.ChoiceField):
    def to_internal_value(self, data):
        if isinstance(data, dict):
            value = data['key']
        else:
            value = data
        if value not in dict(self.choices):
            raise ValidationError(self.error_messages.get('invalid_choice', '不在枚举范围内'))
        return value

    def to_representation(self, value):
        verbose = dict(self.choices).get(value)
        return {'key': value, 'verbose': verbose}