from bank_controller.models import *
from bank_controller.validators import amount_validator, to_account_validator, from_account_validator



# General

def set_ignore_status( obj ):
    """
        Sets the value 'True' for the field 'is_ignor'.
        Designed for model objects ( Purchase, Transfer and Message ).
        It is recommended not to use directly.
    """

    obj.is_ignore = True 
    obj.save()

def set_ignore_status_for_queryset( queryset = None, model = None ):
    """
        Sets the ignore status for the queryset model.
        If queryset is not specified, then sets the ignore status for all records of the specified model.
    """

    assert queryset or model

    if queryset:
        for obj in queryset:
            obj.is_ignore = True
            obj.save()
    if model:
        for obj in model.objects.all():
            obj.is_ignore = True
            obj.save()



# Cash operation

def money_rederection( from_account, to_account, amount, user ):
    """
        Redirects money from "from account" to "to account"
    """

    # Emergency data check

    amount_validator( amount, from_account )
    to_account_validator( to_account, from_account.pk )
    from_account_validator( from_account, user )


    from_account.balance -= amount
    to_account.balance += amount

    from_account.save()
    to_account.save()

def cash_withdrawal( account, amount ):
    """
        Withdraws money from the specified account, returns True if successful, False otherwise
    """

    try:
        amount_validator( amount, account )

        account.balance -= amount
        account.save()

        return True
    except:
        return False
    
# Message

def create_message( account, content ):
    """
        Creates a message
    """

    Message.objects.create(
        account = account,
        content = content,
    )
