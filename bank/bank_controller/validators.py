from rest_framework.exceptions import ValidationError

from .models import *

def account_type_validator( value, user ):
    # Checking if the user has this type of cash account

    for cash_account in user.cash_accounts.all():
        if cash_account.account_type == value:
            raise ValidationError( detail = f'You already have an account type "{value}"' )

    return value

def from_account_validator( value, user ):
    # Checks if the account belongs to this user

    user_accounts = user.cash_accounts.all()

    if value not in ( user_accounts ):
        raise ValidationError( detail = 'Enter your account ID' )
    
    return value

def to_account_validator( to_account, from_account ):
    # Checking for equality between to_account and from_account

    if to_account.pk == int(from_account):
        raise ValidationError( detail = "Fields 'to_account' and 'from_account' cannot be equal" )

    return to_account

def amount_validator( value, account ):
    # Checking if the account has the required amount
    
    if value > account.balance:
        raise ValidationError( detail = 'Not enough money on account' )
    
    return value

def pin_validator( value, account ):
    # Checks the correctness of the entered data

    try:
        value = int(value)
    except ValueError:
        raise ValidationError( detail = 'Enter correct PIN' )

    if value < 1000 or value > 9999:
        raise ValidationError( detail = 'Enter correct PIN' )

    # Checks if the pin is valid for the specified account

    if value != account.pin:
        raise ValidationError( detail = 'Invalid PIN' )
    
    return value
