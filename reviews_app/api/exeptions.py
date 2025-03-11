from rest_framework.exceptions import APIException


class UserUnauthenticated(APIException):
    status_code = 401
    default_detail = 'Unauthorized. Der Benutzer muss authentifiziert sein und ein Kundenprofil besitzen.'
    default_code = 'unauthenticated'


class UserHasAlreadyReview(APIException):
    status_code = 403
    default_detail = 'Forbidden. Ein Benutzer kann nur eine Bewertung pro Geschäftsprofil abgeben.'
    default_code = 'forbidden'