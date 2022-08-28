from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView

from .models import *
from .serializers import *



# Cash account views

class CreateCashAccountView( CreateAPIView ):
    """
        View for create cash account
    """
    
    serializer_class = CreateCashAccountSerializer
    
class RetrieveCashAccountView( RetrieveAPIView ):
    """
        View for displaying cash account
    """

    serializer_class = RetrieveCashAccountSerializer

    def get_queryset(self):
        return CashAccount.objects.filter( owner = self.request.user )


# Transfer views

class CreateTransferView( CreateAPIView ):
    """
        View for create transfer
    """

    serializer_class = CreateTransferSerializer


# Purchase views

class CreatePurchaseView( CreateAPIView ):
    """
        View for create purchase
    """

    serializer_class = CreatePurchaseSerializer

# Credit view

class CreateCreditView( CreateAPIView ):
    """
        View for create credit
    """

    serializer_class = CreateCreditSerializer

class UpdateAmountReturnedOfCreditView( UpdateAPIView ):
    """
        View to pay part of the credit
    """

    serializer_class = UpdateAmountReturnedOfCreditSerializer

    def get_object(self):
        return get_object_or_404( Credit, account = self.request.user.cash_account )