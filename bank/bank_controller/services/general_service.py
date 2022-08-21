from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist



def get_or_raise_validation_error( model, exception_message ,**kwargs ):
    """
        Returns a single model object, or reports absence as a validation error
    """

    try:
        return model.objects.get( **kwargs )
    except ObjectDoesNotExist:
        raise ValidationError( detail = exception_message )