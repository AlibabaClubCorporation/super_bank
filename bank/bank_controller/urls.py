from django.urls import path

from .views import *


urlpatterns = [
    # Cash account urls

    path( 'cash-accounts/', ListCashAccountView.as_view(), name = 'cash_account-list' ),
    path( 'cash-accounts/create/', CreateCashAccountView.as_view(), name = 'cash_account-create' ),
    path( 'cash-accounts/<slug:account_type>/', RetrieveCashAccountView.as_view(), name = 'cash_account-retrieve' ),

    # Transfer urls

    path( 'transfers/create/', CreateTransferView.as_view(), name = 'transfer-create' ),

    # Purchase urls

    path( 'purchase/create/', CreatePurchaseView.as_view(), name = 'purchase-create' ),
]