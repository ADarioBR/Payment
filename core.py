"""
Module for manage payment task
"""

from stripe.error import StripeError
from project.payment.stripe.util_stripe import UtilStripe
from raven.contrib.django.raven_compat.models import client


class PaymentTask:
    stripe = UtilStripe()

    def update(self, data, customer_id):
        """
        Update a payment
        :param data:
        :param customer_id:
        :return:
        """
        payment_type = data.get('type')
        try:
            result = None
            if payment_type == "C":
                result = self.stripe.update_card(
                    customer_stripe_id=customer_id,
                    card_id=data.get('card_id'),
                    name=data.get('card_holder'),
                    exp_month=data.get('card_exp_month'),
                    exp_year=data.get('card_exp_year')
                )
            elif payment_type == "B":
                result = self.stripe.update_bank(
                    customer_stripe_id=customer_id,
                    bank_id=data.get('bk_id'),
                    bk_holder=data.get('bk_holder'),
                    bk_type=data.get('bk_type'),
                )
            return True, result
        except StripeError as e:
            client.captureException()
            return False, e

    def delete(self, data, customer_id):
        """
        Delete a payment
        :param data:
        :param customer_id:
        :return:
        """
        payment_type = data.get('type')
        result = None
        try:
            if payment_type == "C":
                result = self.stripe.delete_card(
                    customer_stripe_id=customer_id,
                    card_id=data.get('card_id'),
                )
            elif payment_type == "B":
                result = self.stripe.delete_bank(
                    customer_stripe_id=customer_id,
                    bank_id=data.get('bk_id'),
                )
            return True, result
        except StripeError as e:
            client.captureException()
            return False, e
