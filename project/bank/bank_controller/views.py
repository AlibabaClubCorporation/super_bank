from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView

from .models import *
from .serializers import *
from .mixins.view_mixins import ClearHistoryMixinView



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

    def get_object(self):
        return get_object_or_404( CashAccount, owner = self.request.user )


# Transfer views

class CreateTransferView( CreateAPIView ):
    """
        View for create transfer
    """

    serializer_class = CreateTransferSerializer

class ClearTransferHistoryView( ClearHistoryMixinView ):
    """
        View for clear transfers history
    """

    model = Transfer

# Purchase views

class CreatePurchaseView( CreateAPIView ):
    """
        View for create purchase
    """

    serializer_class = CreatePurchaseSerializer

class ClearPurchaseHistoryView( ClearHistoryMixinView ):
    """
        View for clear purchases history
    """

    model = Purchase

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

# Message view

class ClearMessageHistoryView( ClearHistoryMixinView ):
    """
        View for clear messages history
    """

    model = Message