from rest_framework import serializers

from bank_controller.services.database_service import get_or_raise_validation_error
from bank_controller.services.general_bank_service import money_rederection
from bank_controller.validators import pin_validator, amount_validator
from bank_controller.models import *



class TransactionsSerializerMixin( serializers.Serializer ):
    """
        Mixin serializer designed to be inherited from serializers that require processing and checking the PIN field
    """

    pin = serializers.IntegerField(
        read_only = True,
    )

    def validate_pin(self, value):
        try:
            account_pk = self.initial_data['account']
        except:
            account_pk = self.initial_data['from_account']
        
        account = get_or_raise_validation_error(
            model = CashAccount,
            exception_message = 'Failed to retrieve account information.',

            # kwargs
            pk = account_pk,
            owner = self.context['request'].user
        )

        return pin_validator( value, account )

    def validate_amount(self, value):
        try:
            account_pk = self.initial_data['account']
        except:
            account_pk = self.initial_data['from_account']

        account = get_or_raise_validation_error(
            model = CashAccount,
            exception_message = 'Failed to retrieve account information.',

            # kwargs
            pk = account_pk,
            owner = self.context['request'].user
        )

        return amount_validator( value, account )

    def validate(self, attrs):
        self.validate_pin( self.initial_data['pin'] )

        return super().validate(attrs)

    def create(self, validated_data):
        from_account = validated_data['from_account']
        to_account = validated_data['to_account']
        amount = validated_data['amount']
        user = self.context['request'].user

        money_rederection(
            to_account = to_account,
            from_account = from_account,
            amount = amount,
            user = user
        )

        return super().create(validated_data)