from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class CustomUser( AbstractUser ):
    """
        model of custom user
    """

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'gender',
        'birth_date',
        'city',
        'adress',
        'email',
    ]

    GENDERS = (
        ( 'm', 'male' ),
        ( 'f', 'female'),
    )

    gender = models.CharField(
        max_length = 1,
        choices = GENDERS,
    )

    city = models.CharField( max_length = 255, )
    adress = models.CharField( max_length = 255, )

    email = models.EmailField( unique = True )

    birth_date = models.DateField()



class CashAccount( models.Model ):
    """
        Model of cash account
    """

    ACCOUNT_TYPES = (
        ( 'd', 'debit' ),
        ( 'c', 'credit' ),
    )

    owner = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'cash_accounts',
    )

    balance = models.IntegerField( default = 0 )

    creation_date = models.DateField( auto_now_add = True )
    is_blocked = models.BooleanField( default = False )

    account_type = models.CharField(
        max_length = 1,
        choices = ACCOUNT_TYPES,
    )

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
        decimal_places=2
    )

    comment = models.CharField(
        max_length = 255,

        blank = True,
        null = True,
    )

    creation_date = models.DateTimeField( auto_now_add = True )


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
        decimal_places=2
    )

    creation_date = models.DateTimeField( auto_now_add = True )