from .exeptions import *
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def validate_username(username):
    """
    Validate the username. Check if it is alphanumeric and does not contain spaces.
    """
    if " " in username:
        raise UsernameContainsSpace()
    if User.objects.filter(username=username).exists():
        raise UsernameExistAlready()
    return username
    

def validate_email_address(email, user=None):
    """
    Validate the email address. Check if it is already in use or if it is incorrectly formatted.
    """
    if user and user.email == email:
        return email

    if User.objects.filter(email=email).exists():
        raise EmailExistAlready()
        
    try:
        validate_email(email) 
    except ValidationError:
        raise EmailIncorrect()
        
    return email
    
    
def validate_password(password, repeated_password):
    """
    Validate the password. Check if it is at least 8 characters long and contains at least one digit.
    """
    if password != repeated_password:
        raise PasswordNotMatch()