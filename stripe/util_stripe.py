"""
Stripe module
"""

import stripe
from django.conf import settings

# set the stripe secret key
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', None)


class UtilStripe:
    """
    A manager for stripe payment
    """

    def __init__(self, customer_stripe_id):
        """Return a stripe Customer object."""
        self.customer = stripe.Customer.retrieve(customer_stripe_id)

    def update_bank(self, bank_id, bk_holder=None, bk_type=None):
        """
        Update stripe bank
        :param bank_id: str
        :param bk_holder: str
        :param bk_type: str
        :return bank: object
        """
        bank_account = self.customer.sources.retrieve(bank_id)
        if bk_holder:
            bank_account.account_holder_name = bk_holder
        if bk_type:
            bank_account.account_holder_type = bk_type
        bank = bank_account.save()
        return bank

    def delete_payment(self, payment_id):
        """
        Delete a payment source
        :param payment_id: str
        :return payment: object
        """
        payment = self.customer.sources.retrieve(payment_id).delete()
        return payment

    def update_card(self, card_id, name=None, exp_month=None, exp_year=None):
        """
        Update a stripe card
        :param card_id: str
        :param name: str
        :param exp_month: str
        :param exp_year: str
        :return card: object
        """
        card = self.customer.sources.retrieve(card_id)
        if name:
            card.name = name
        if exp_month:
            card.exp_month = exp_month
        if exp_year:
            card.exp_year = exp_year
        card = card.save()
        return card
