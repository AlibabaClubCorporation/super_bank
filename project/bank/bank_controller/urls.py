from django.urls import path

from .views import *


urlpatterns = [
    # Cash account urls

    path( 'cash-account/create/', CreateCashAccountView.as_view(), name = 'cash_account-create' ),
    path( 'cash-account/', RetrieveCashAccountView.as_view(), name = 'cash_account-retrieve' ),

    # Transfer urls

    path( 'transfers/create/', CreateTransferView.as_view(), name = 'transfer-create' ),
    path( 'transfers/clear/', ClearTransferHistoryView.as_view(), name = 'transfer-clear' ),

    # Purchase urls

    path( 'purchases/create/', CreatePurchaseView.as_view(), name = 'purchase-create' ),
    path( 'purchases/clear/', ClearPurchaseHistoryView.as_view(), name = 'purchase-clear' ),

    # Message urls

    path( 'messages/clear/', ClearMessageHistoryView.as_view(), name = 'message-clear' ),

    # Credit urls

    path( 'credits/create/', CreateCreditView.as_view(), name = 'credit-create' ),
    path( 'credits/payment/', UpdateAmountReturnedOfCreditView.as_view(), name = 'credit-update-amount-returned' ),
]