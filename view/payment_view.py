"""
This module contain an API view to manage the customer
stripe payment
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from serializer.payment_serializer import PaymentSerializer
from core import PaymentTask


class PaymentView(APIView):
    """
    Handle http method request for stripe payment
    """
    # create the payment serializer
    payment_serializer = PaymentSerializer
    # create the payment manager
    core = PaymentTask()

    def post(self, request):
        """
        Update a customer payment

        request.data must contain
        type: 'C' if is a car or 'B' if is a bank
        card_id: stripe card id if type is 'C'
        card_holder: Name on card
        card_exp_month: Card expiration month
        bk_id: stripe bank id if type is 'B'
        bk_holder: Bank holder
        bk_type: Bank type

        :param request:
        :return:
        """
        # initialize the payment serializer with the request data
        payment = self.payment_serializer(data=request.data)
        # check if the serializer is valid
        if payment.is_valid():
            # obtain the user stripe_id
            stripe_id = request.user.customer.stripe_id
            # update the stripe payment
            valid, result = self.core.update(payment.validated_data, stripe_id)
            # if is valid return a OK (200) response and the payment updated data
            if valid:
                return Response(result, status=status.HTTP_200_OK)
            # else return a bad request(400) response and a json with the error
            else:
                error = {"error": "Can't update the stripe payment"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

        # if the serializer payment is not valid return a bad request(400)
        # response and a json with the serializer errors
        return Response(payment.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Delete a customer payment

        request.data must contain
        type:'C' if is a card or 'B' if is a bank
        bk_id:stripe bank id if type is 'B'
        card_id:stripe card id if type is 'C'

        :param request:
        :return:
        """
        # initialize the payment serializer with the request data
        payment = self.payment_serializer(data=request.data)
        # check if the serializer is valid
        if payment.is_valid():
            # obtain the user stripe_id
            stripe_id = request.user.customer.stripeID
            # delete the stripe payment
            valid, result = self.core.delete(payment.validated_data, stripe_id)
            # if is valid return a OK (200) response and the payment deleted data
            if valid:
                return Response(result, status=status.HTTP_200_OK)
            # else return a bad request(400) response and a json with the error
            else:
                error = {"error": "Can't delete the stripe payment"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        # if the serializer payment is not valid return a bad request(400)
        # response and a json with the serializer errors
        return Response(payment.errors, status=status.HTTP_400_BAD_REQUEST)
