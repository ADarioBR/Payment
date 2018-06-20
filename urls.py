from django.conf.urls import url

from project.payment.view.payment_view import PaymentView

urlpatterns = [
    url(r'^payment/', PaymentView.as_view(), name='payment'),
]

