from django.urls import path

from .views import *


urlpatterns = [
    # Cash account urls

    path( 'cash-accounts/create/', CreateCashAccountView.as_view(), name = 'cash_account-create' ),
    path( 'cash-accounts/<int:pk>/', RetrieveCashAccountView.as_view(), name = 'cash_account-retrieve' ),

    # Transfer urls

    path( 'transfers/create/', CreateTransferView.as_view(), name = 'transfer-create' ),

    # Purchase urls

    path( 'purchases/create/', CreatePurchaseView.as_view(), name = 'purchase-create' ),

    # Credit urls

    path( 'credits/create/', CreateCredirView.as_view(), name = 'credit-create' ),
]