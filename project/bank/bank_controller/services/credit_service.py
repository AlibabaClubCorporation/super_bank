from bank_controller.models import *
from .general_bank_service import *

from math import ceil
import datetime


def create_credit( amount, account, parts ):
    """
        Creates a loan, and then sends the required amount to the debtor
    """

    instance = Credit.objects.create(
        amount = amount,
        account = account,
        parts = parts,
        percent = parts,
    )

    account.balance += amount
    account.save()

    return instance


def payment_part_credit( credit, amount ):
    """
        Withdraws money for part of the credit, returns True if successful, False otherwise
    """

    if cash_withdrawal( credit.account, amount ):
        credit.amount_returned += amount
        credit.save()

        Purchase.objects.create(
            account = credit.account,
            amount = amount,
            merchant = f'Credit | PK: {credit.pk}',
        )

        message_content = f'Your account has been debited for part of the credit'

        credit.account.is_blocked = False
        credit.account.save()

        create_message( credit.account, message_content )
        
        # If the loan is paid in full, deletes the record and sends a message
        credit_repayment_check( credit )

        return True

    return False


def calc_credit_amount_with_percent( obj ):
    """
        Returns the credit amount including percents
    """

    amount = obj.amount
    percent = obj.percent + int( obj.is_increased_percentage )

    return amount + ( amount / 100 ) * percent

def calc_remaining_amount_to_repay_credit( obj ):
    """
        Returns the amount required to fully repay the credit
    """

    return calc_credit_amount_with_percent( obj ) - obj.amount_returned

def calc_amount_required_to_pay_one_credit_part( obj ):
    """
        Returns the amount required to pay one ( next ) part of the credit
    """

    amount_to_pay_one_part = calc_credit_amount_with_percent( obj ) / obj.parts
    amount_to_fully_repay = calc_remaining_amount_to_repay_credit( obj )

    if amount_to_fully_repay > amount_to_pay_one_part:
        return amount_to_pay_one_part
    
    return amount_to_fully_repay
    

def calc_parts_remaining_to_pay_credit( obj ):
    """
        Returns the number of installments left to fully repay the credit
    """

    return ceil( calc_remaining_amount_to_repay_credit( obj ) / calc_amount_required_to_pay_one_credit_part( obj ) )

def calc_number_paid_credit_parts( obj ):
    """
        Return the number of paid installments of the credit
    """

    return obj.parts - calc_parts_remaining_to_pay_credit( obj )

def calc_payment_time_limit( obj ):
    """
        Returns the time until the next payment
    """

    amount_paid_parts_credit = calc_number_paid_credit_parts( obj )
    
    return obj.creation_date + datetime.timedelta( minutes = amount_paid_parts_credit + int( obj.is_increased_percentage ) + 1 )

def credit_repayment_check( credit ):
    """
        Checks whether the loan is paid or not, if paid:
        - Sends a message about the payment of the credit to the debtor
        - Deletes a credit entry
    """

    if credit.amount_returned == calc_credit_amount_with_percent( credit ):
        message_content = f'You have successfully paid the loan with ID "{credit.pk}"'
        create_message( credit.account, message_content )

        credit.delete()

        return True
    
    return False


def checking_payment_part_credit( credit ):
    """
        Checks the payment status of a portion of a loan.
        If the operation is successful:
        - Sends a message about successful payment.
        - If the user has been blocked - unblocks him.
        If the operation is not successful:
        - Sends the required message
        - Increases the percentage of the loan rate for the first non-payment of the loan part
        - Blocks the user for a second or more non-payment of the loan
    """

    if not payment_part_credit( credit, calc_amount_required_to_pay_one_credit_part( credit ) ):
        if not credit.is_increased_percentage:
            credit.is_increased_percentage = True
            credit.save()
            message_content = f'Due to non-payment of the credit, the interest rate was increased for the credit with the identifier "{credit.pk}"'
            create_message( credit.account, message_content )
        else:
            if not credit.account.is_blocked:
                credit.account.is_blocked = True
                credit.account.save()

                message_content = f'Your account is blocked due to non-payment of the credit. To unlock the account, you need to invest the amount ( { calc_amount_required_to_pay_one_credit_part(credit) } ), after withdrawing the money, the account will be unlocked'
                create_message( credit.account, message_content )


def checking_credits_status():
    """
        Checks all existing credits.
        Sends a message and increases the percentage if the credit is not paid on time.
        Blocks the debtor's account if the credit has not been paid twice.
        Withdraws money from the account if it is enough to repay the necessary part of the credit.
    """

    # Collection of all credits
    credits = Credit.objects.all().select_related( 'account' )

    # Go through all the credit to check
    for credit in credits:
        # Calculates the time to make the next payment

        payment_time_limit = calc_payment_time_limit( credit )

        # The condition will return True when it is necessary to repay part of the credit
        if payment_time_limit < datetime.datetime.now( tz = datetime.timezone.utc ):
            checking_payment_part_credit(credit)
