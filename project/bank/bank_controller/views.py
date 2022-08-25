from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from .models import *
from .serializers import *
from .tasks import add as func



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

    def get(self, request, *args, **kwargs):
        func.delay()
        return super().get(request, *args, **kwargs)


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

class CreateCredirView( CreateAPIView ):
    """
        View for create credit
    """

    serializer_class = CreateCreditSerializer