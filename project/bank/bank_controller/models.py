from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class CustomUser( AbstractUser ):
    """
        model of custom user
    """

    REQUIRED_FIELDS = [
        # 'first_name',
        # 'last_name',
        # 'gender',
        # 'birth_date',
        # 'city',
        # 'adress',
        'email',
    ]

    GENDERS = (
        ( 'm', 'male' ),
        ( 'f', 'female'),
    )

    gender = models.CharField(
        max_length = 1,
        choices = GENDERS,

        default = 'm'
    )

    city = models.CharField( max_length = 255, default = 'm' )
    adress = models.CharField( max_length = 255, default = 'm' )

    email = models.EmailField( unique = True, )

    birth_date = models.DateField(default = '2005-10-05')



class CashAccount( models.Model ):
    """
        Model of cash account
    """

    owner = models.OneToOneField(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'cash_account',
    )

    balance = models.IntegerField( default = 0, )

    creation_date = models.DateField( auto_now_add = True, )
    is_blocked = models.BooleanField( default = False, )

    pin = models.PositiveSmallIntegerField()



class Transfer( models.Model ):
    """
        Model of transfer
    """

    from_account = models.ForeignKey(
        to = CashAccount,
        on_delete = models.CASCADE,
        related_name = 'sent_transfers',
    )
    to_account = models.ForeignKey(
        to = CashAccount,
        on_delete = models.CASCADE,
        related_name = 'received_transfers',
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    comment = models.CharField(
        max_length = 255,

        blank = True,
        null = True,
    )

    creation_date = models.DateTimeField( auto_now_add = True, )


class Purchase( models.Model ):
    """
        Model of purchase
    """

    account = models.ForeignKey(
        to = CashAccount,
        on_delete = models.CASCADE,
        related_name = 'purchases',
    )

    merchant = models.CharField(
        max_length = 255,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    creation_date = models.DateTimeField( auto_now_add = True, )


class Credit( models.Model ):
    """
        Model of credit

        Rules under which the credit works:
        - 1 user - maximum 1 credit.
        - Once a month (per minute during development/testing) the debtor's account is debited with the amount of credit divided by the number of parts of the loan and multiplied by the percentage of the loan (usually the percentage is equal to the number of parts, but if the "is_increased_percentage" flag is set to "True", then the percentage increased by 1).
        - If you miss a payment once, a message about it comes, and the "is_increased_percentage" flag becomes True for the entire duration of the loan.
        - If you miss the payment 2 times, you will receive a message about this, after the account is blocked (Can not make payment transactions), until the necessary amount to pay part of the loan is on the account (For example, if the amount comes from another account).
        - If the account has been blocked, but part of the credit. paid, the account is considered unlocked.
        * Important note: The "is_increased_percentage" flag remains True .
        - After the full payment of the loan, the loan data is deleted.
    """

    PARTS_CHOISES = (
        ( 1, 1 ),
        ( 3, 3 ),
        ( 5, 5 ),
    )

    amount = models.DecimalField(
        max_digits = 7,
        decimal_places = 2,
    )

    account = models.OneToOneField(
        to = CashAccount,
        on_delete = models.PROTECT,
        related_name = 'credit',
    )

    creation_date = models.DateTimeField( auto_now_add = True, )

    percent = models.PositiveSmallIntegerField(
        default = 1,
        choices = PARTS_CHOISES,
    )
    parts = models.PositiveSmallIntegerField(
        default = 1,
    )

    amount_returned = models.DecimalField(
        max_digits = 7,
        decimal_places = 2,
        
        default = 0,
    )

    is_increased_percentage = models.BooleanField( default = False, )


class Message( models.Model ):
    """
        Model of message.
        Usually contains information related to lending, or account blocking.
    """

    content = models.CharField( max_length = 512, )

    account = models.ForeignKey(
        to = CashAccount,
        on_delete = models.CASCADE,
        related_name = 'messages',
    )

    creation_date = models.DateTimeField( auto_now_add = True, )