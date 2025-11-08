from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from users.serializers import PaymentSerializer
from users.models import Payment


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    filterset_fields = ('course', 'lesson')
    search_fields = ['payment_method']
    ordering_fields = ('date',)

