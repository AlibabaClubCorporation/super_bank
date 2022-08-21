from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from .validators import *
from .mixins.serializer_mixins import *


# Tranfer serializers

class CreateTransferSerializer( TransactionsSerializerMixin, serializers.ModelSerializer ):
    """
        Serializer for create transfer
    """

    class Meta:
        model = Transfer
        fields = ( 'from_account', 'to_account', 'amount', 'comment', 'creation_date', 'pin' )
        read_only_fields = ( 'creation_date', )


    def validate_from_account(self, value):
        user = self.context['request'].user

        return from_account_validator( value, user )
    
    def validate_to_account(self, value):
        return to_account_validator( value, self.initial_data['from_account'] )

    def validate(self, attrs):
        return super().validate(attrs)


class DisplayTransferSerializer( serializers.ModelSerializer ):
    """
        Serializer for displaying transfers
    """

    class Meta:
        model = Transfer
        fields = '__all__'


# Purchase serializers


class CreatePurchaseSerializer( TransactionsSerializerMixin, serializers.ModelSerializer ):
    """
        Serializer for create purchase
    """

    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ( 'creation_date', )
    

    def validate_account(self, value):
        user = self.context['request'].user

        return from_account_validator( value, user )


class DisplayPurchaseSerializer( serializers.ModelSerializer ):
    """
        Serializer for displaying purchases
    """

    class Meta:
        model = Purchase
        fields = '__all__'


# Cash account serializers

class CreateCashAccountSerializer( serializers.ModelSerializer ):
    """
        Serializer for create cash account
    """

    owner = serializers.HiddenField( default = serializers.CurrentUserDefault() )

    class Meta:
        model = CashAccount
        fields = '__all__'
        read_only_fields = ( 'balance', 'creation_date', 'is_blocked',)


    def validate_pin(self, value):
        # Checking the data type, and entering the desired interval

        if type(value) != int or len(str(value)) != 4:
            raise ValidationError( detail = 'Enter a pin from 1000 to 9999' )
        
        return value

    def validate_account_type(self, value):
        user = self.context['request'].user

        return account_type_validator( value, user )


class ListCashAccountSerializer( serializers.ModelSerializer ):
    """
        Serializer for display list cash accounts
    """

    class Meta:
        model = CashAccount
        fields = ( 'account_type', 'balance', 'is_blocked', )

class RetrieveCashAccountSerializer( serializers.ModelSerializer ):
    """
        Serializer for display cash account
    """

    history = serializers.SerializerMethodField()

    class Meta:
        model = CashAccount
        fields = ( 'account_type', 'balance', 'is_blocked', 'creation_date', 'pin', 'history' )
    

    def get_history( self, obj ):
        # Receive all transfers and purchases
        purchases = DisplayPurchaseSerializer( data = obj.purchases.all(), many = True )
        sent_transfers = DisplayTransferSerializer( data = obj.sent_transfers.all(), many = True )
        receiver_transfers = DisplayTransferSerializer( data = obj.received_transfers.all(), many = True)

        purchases.is_valid()
        sent_transfers.is_valid()
        receiver_transfers.is_valid()

        return {
            'purchases' : purchases.data,
            'transfers' : {
                'sent' : sent_transfers.data,
                'received' : receiver_transfers.data,
                }
            }
