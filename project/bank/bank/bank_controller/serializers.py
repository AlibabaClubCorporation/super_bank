from re import L
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from .validators import *
from .mixins.serializer_mixins import *
from .services.general_bank_service import *



# Message serializer

class DisplayMessageSerializer( serializers.ModelSerializer ):
    """
        Serializer for displaying message
    """

    class Meta:
        model = Message
        fields = ( 'content', 'creation_date' )

# Credit serializer

class CreateCreditSerializer( TransactionsSerializerMixin, serializers.ModelSerializer ):
    """
        Serializer for create credit
    """

    class Meta:
        model = Credit
        fields = ( 'amount', 'account', 'parts', 'pin' )

    def validate_amount(self, value):
        if value < 1000:
            raise ValidationError( 'Loan too small. Loan amount must be at least 1000' )
        
        return value
    
    def validate_account(self, value):
        user = self.context['request'].user

        return from_account_validator( value, user )

    def create(self, validated_data):
        parts = validated_data['parts']
        amount = validated_data['amount']
        account = validated_data['account']

        instance = create_credit( amount, account, parts )

        return instance

class DisplayCreditSerializer( serializers.ModelSerializer ):
    """
        Serializer for display credit
    """

    amount_with_percent = serializers.SerializerMethodField()
    number_of_parts_left = serializers.SerializerMethodField()
    amount_to_pay_one_part = serializers.SerializerMethodField()
    amount_to_fully_repay = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        exclude = ( 'account', )
        

    def get_amount_with_percent( self, obj ):
        return calc_credit_amount_with_percent( obj )

    def get_number_of_parts_left( self, obj ):
        return calc_parts_remaining_to_pay_credit( obj )

    def get_amount_to_pay_one_part( self, obj ):
        return calc_amount_required_to_pay_one_credit_part( obj )

    def get_amount_to_fully_repay( self, obj ):
        return calc_remaining_amount_to_repay_credit( obj )

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
        read_only_fields = ( 'balance', 'creation_date', 'is_blocked', )


    def validate_pin(self, value):
        # Checking the data type, and entering the desired interval

        if type(value) != int or len(str(value)) != 4:
            raise ValidationError( detail = 'Enter a pin from 1000 to 9999' )
        
        return value

    def validate_owner(self, value):
        return no_account_validator( value )


class RetrieveCashAccountSerializer( serializers.ModelSerializer ):
    """
        Serializer for display cash account
    """

    history = serializers.SerializerMethodField()
    credit = DisplayCreditSerializer()
    messages = DisplayMessageSerializer( many = True )

    class Meta:
        model = CashAccount
        fields = ( 'balance', 'is_blocked', 'creation_date', 'pin', 'history', 'credit' , 'messages' )
    

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
        
        


        

