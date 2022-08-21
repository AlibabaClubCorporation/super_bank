from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from .models import *
from .serializers import *



# Cash account views

class CreateCashAccountView( CreateAPIView ):
    """
        View for create cash account
    """
    
    serializer_class = CreateCashAccountSerializer

class ListCashAccountView( ListAPIView ):
    """
        View for displaying list cash accounts
    """

    serializer_class = ListCashAccountSerializer

    def get_queryset(self):
        return CashAccount.objects.filter( owner = self.request.user )
    
class RetrieveCashAccountView( RetrieveAPIView ):
    """
        View for displaying cash account
    """

    serializer_class = RetrieveCashAccountSerializer

    def get_queryset(self):
        return CashAccount.objects.filter( owner = self.request.user )
    
    def get_object(self):
        # Redefined to get the correct account based on the user who sent the request and the values from the request

        queryset = self.filter_queryset( self.get_queryset() )

        filter_kwargs = { 'account_type' : self.kwargs.get('account_type') }
        obj = get_object_or_404( queryset, **filter_kwargs )

        return obj


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