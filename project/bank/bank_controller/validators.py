from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from .models import *


def from_account_validator( value, user ):
    # Checks if the account belongs to this user

    if value != user.cash_account:
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
    if value < 1:
        raise ValidationError( detail = "You cannot make a transaction for an amount less than 1" )
    
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

def no_account_validator( value ):
    # Checking if a user has an account

    try:
        value.cash_account
        raise ValidationError( 'You already have your own account' )
    except ObjectDoesNotExist:
        return value

def id_list_validate( id_list ):
    error_message = None

    # Checking for a list type for id_list

    if type( id_list ) != list:
        error_message = "The 'id_list' parameter must be a list"

    # Checks each list value for a integer type

    for id in id_list:
        if type( id ) != int:
            error_message = 'One of the values in the passed list is not numeric and is not suitable for use as an identifier'
    
    # Returns True if the check succeeded, False if the check failed.

    if error_message:
        return False, error_message
    
    return True, error_message