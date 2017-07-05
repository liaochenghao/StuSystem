# coding: utf-8
from rest_framework import serializers
from admin.models import PaymentAccountInfo
from utils.serializer_fields import VerboseChoiceField


class PaymentAccountInfoSerializer(serializers.ModelSerializer):
    payment = VerboseChoiceField(PaymentAccountInfo.PAYMENT)

    class Meta:
        model = PaymentAccountInfo
        fields = ['id', 'account_number', 'account_name', 'opening_bank', 'payment']