from .exeptions import *
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def validate_username(username):
    if " " in username:
        raise UsernameContainsSpace()
    if User.objects.filter(username=username).exists():
        raise UsernameExistAlready()
    return username
    
def validate_email_address(email):
    if User.objects.filter(email=email).exists():
        raise EmailExistAlready()
        
    try:
        validate_email(email) 
    except ValidationError:
        raise EmailIncorrect()
        
    return email
    
def validate_password(password, repeated_password):
    if password != repeated_password:
        raise PasswordNotMatch()