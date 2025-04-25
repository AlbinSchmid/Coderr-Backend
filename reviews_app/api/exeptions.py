from rest_framework.exceptions import APIException


class UserUnauthenticated(APIException):
    """
    Exception raised when a user is not authenticated.
    """
    status_code = 401
    default_detail = 'Unauthorized. Der Benutzer muss authentifiziert sein.'
    default_code = 'unauthenticated'


class UserUnauthenticatedPost(APIException):
    """
    Exception raised when a user is not authenticated for a POST request.
    """
    status_code = 401
    default_detail = 'Unauthorized. Der Benutzer muss authentifiziert sein und ein Kundenprofil besitzen.'
    default_code = 'unauthenticated'


class UserHasAlreadyReview(APIException):
    """
    Exception raised when a user tries to create a review for a business profile they already reviewed.
    """
    status_code = 403
    default_detail = 'Forbidden. Ein Benutzer kann nur eine Bewertung pro Geschäftsprofil abgeben.'
    default_code = 'forbidden'


class UserIsNotOwnerForDelete(APIException):
    """
    Exception raised when a user tries to delete a review they do not own.
    """
    status_code = 403
    default_detail = 'Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu löschen.'
    default_code = 'forbidden'


class UserIsNotConsumer(APIException):
    """
    Exception raised when a user is not a consumer.
    """
    status_code = 403
    default_detail = 'Forbidden. Der Bentutzer ist kein typ vom Consumer.'
    default_code = 'forbidden'


class UserIsNotOwnerForPatch(APIException):
    """
    Exception raised when a user tries to edit a review they do not own.
    """
    status_code = 403
    default_detail = 'Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu bearbeiten.'
    default_code = 'forbidden'


class ReviewNotFound(APIException):
    """
    Exception raised when a review is not found.
    """
    status_code = 404
    default_detail = 'Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden.'
    default_code = 'not_found'


class BadRequest(APIException):
    """
    Exception raised for a bad request.
    """
    status_code = 400
    default_detail = 'Bad Request. Der Anfrage-Body enthält ungültige Daten.'
    default_code = 'bad_request'