from bank_controller.validators import amount_validator, to_account_validator, from_account_validator



def money_rederection( from_account, to_account, amount, user ):
    # Emergency check for the availability of the required amoun

    amount_validator( amount, from_account )
    to_account_validator( to_account, from_account.pk )
    from_account_validator( from_account, user )


    from_account.balance -= amount
    to_account.balance += amount

    from_account.save()
    to_account.save()