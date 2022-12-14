from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from .validators import *
from .mixins.serializer_mixins import *
from .services.general_bank_service import *
from .services.credit_service import *



# Message serializer

class DisplayMessageSerializer( serializers.ModelSerializer ):
    """
        Serializer for displaying message
    """

    class Meta:
        model = Message
        fields = ( 'content', 'creation_date', 'id', )

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

class UpdateAmountReturnedOfCreditSerializer( TransactionsSerializerMixin ):
    """
        Serializer to pay part of the credit
    """

    amount = serializers.IntegerField()

    class Meta:
        model = Credit
        fields = ( 'amount', )
    
    def validate_amount(self, value):
        remaining_amount_to_repay_credit = calc_remaining_amount_to_repay_credit( self.instance )

        if remaining_amount_to_repay_credit < value:
            raise ValidationError( f"You cannot pay more than what is required to fully repay the loan ( { remaining_amount_to_repay_credit } )" )

        return super().validate_amount( value )

    def update(self, instance, validated_data):
        payment_part_credit( instance, validated_data['amount'] )

        return instance

    
    def to_representation(self, instance):
        if not instance.pk:
            return { 'credit' : 'Has been paid and removed' }

        return DisplayCreditSerializer( instance = instance ).data

class DisplayCreditSerializer( serializers.ModelSerializer ):
    """
        Serializer for display credit
    """

    amount_with_percent = serializers.SerializerMethodField()
    number_of_parts_left = serializers.SerializerMethodField()
    amount_to_pay_one_part = serializers.SerializerMethodField()
    amount_to_fully_repay = serializers.SerializerMethodField()
    amount_paid_parts_credit = serializers.SerializerMethodField()
    payment_time_limit = serializers.SerializerMethodField()
    time_remaining_until_payment = serializers.SerializerMethodField()

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

    def get_amount_paid_parts_credit( self, obj ):
        return calc_number_paid_credit_parts( obj )

    def get_payment_time_limit( self, obj ):
        return calc_payment_time_limit( obj )

    def get_time_remaining_until_payment( self, obj ):
        time_now = datetime.datetime.now( tz = datetime.timezone.utc )

        return calc_payment_time_limit( obj ) - time_now

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
        exclude = ( 'is_ignore' )


# Purchase serializers


class CreatePurchaseSerializer( TransactionsSerializerMixin, serializers.ModelSerializer ):
    """
        Serializer for create purchase
    """

    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ( 'creation_date', 'is_ignore', )
    

    def validate_account(self, value):
        user = self.context['request'].user

        return from_account_validator( value, user )

    def create(self, validated_data):
        account = validated_data['account']
        amount = validated_data['amount']

        cash_withdrawal(
            account = account,
            amount = amount,
        )

        return super().create(validated_data)


class DisplayPurchaseSerializer( serializers.ModelSerializer ):
    """
        Serializer for displaying purchases
    """

    class Meta:
        model = Purchase
        exclude = ( 'is_ignore', )


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
    messages = serializers.SerializerMethodField()

    class Meta:
        model = CashAccount
        fields = ( 'balance', 'is_blocked', 'creation_date', 'pin', 'history', 'credit' , 'messages' )
    

    def get_messages( self, obj ):
        serializer = DisplayMessageSerializer(
            data = obj.messages.filter( is_ignore = False ),
            many = True
        )
        serializer.is_valid()

        return serializer.data

    def get_history( self, obj ):
        # Receive all transfers and purchases
        purchases = DisplayPurchaseSerializer(
            data = obj.purchases.filter( is_ignore = False ),
            many = True
        )
        sent_transfers = DisplayTransferSerializer(
            data = obj.sent_transfers.filter( is_ignore = False ),
            many = True
        )
        receiver_transfers = DisplayTransferSerializer(
            data = obj.received_transfers.filter( is_ignore = False ),
            many = True
        )

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
        
        


        

