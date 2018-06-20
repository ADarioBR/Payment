"""
Serializer for payment request
"""

from rest_framework.fields import CharField, BooleanField, DateTimeField
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError


class PaymentSerializer(Serializer):
    """
    Payment serializer
    """
    type = CharField(required=True, allow_null=False, max_length=50)
    card_id = CharField(required=False, max_length=50, allow_blank=True)
    card_holder = CharField(required=False, max_length=50, allow_blank=True)
    card_exp_month = CharField(required=False, max_length=50, allow_blank=True)
    card_exp_year = CharField(required=False, max_length=50, allow_blank=True)
    bk_holder = CharField(required=False, max_length=50, allow_blank=True)
    bk_type = CharField(required=False, max_length=50, allow_blank=True)
    bk_id = CharField(required=False, max_length=50, allow_blank=True)

    def validate(self, attrs):
        """
        Validate the serializer fields
        :param attrs:
        :return attrs:
        """
        # check if the type field is a card(C)
        if attrs['type'] == 'C':
            # rise an exception if the card_id is empty
            if attrs['card_id'] == "":
                msg = 'Card id is empty.'
                raise ValidationError(msg)
        # check if the type field is a bank (B)
        elif attrs['type'] == 'B':
            # rise an exception if the bk_id is empty
            if attrs['bk_id'] == "":
                msg = 'Bank id is empty.'
                raise ValidationError(msg)
        else:
            msg = 'Invalid payment type.'
            raise ValidationError(msg)
        return attrs
