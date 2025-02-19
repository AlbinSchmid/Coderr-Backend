from rest_framework.exceptions import APIException

class UsernameContainsSpace(APIException):
    status_code = 400
    default_detail = "Benutzername darf kein Leerzeichen enthalten."
    default_code = "username_invalid"

class UsernameExistAlready(APIException):
    status_code = 409
    default_detail = "Benutzername existiert bereits."
    default_code = "username_invalid"

class EmailIncorrect(APIException):
    status_code = 400
    default_detail = "Bitte geben Sie eine gültige Email an."
    default_code = "email_invalid"

class EmailExistAlready(APIException):
    status_code = 409
    default_detail = "Diese Email existiert bereits."
    default_code = "email_invalid"

class PasswordNotMatch(APIException):
    status_code = 400
    default_detail = "Passwörter müssen übereinstimmen."
    default_code = "password_not_match"

class Unauthorized(APIException):
    status_code = 403
    default_detail = "Sie sind nicht Berechtig."
    default_code = "unauthorized"

class UserNotFound(APIException):
    status_code = 404
    default_detail = "User wurde nicht gefunden."
    default_code = "not_found"
