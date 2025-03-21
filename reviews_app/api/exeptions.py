from rest_framework.exceptions import APIException


class UserUnauthenticated(APIException):
    status_code = 401
    default_detail = 'Unauthorized. Der Benutzer muss authentifiziert sein.'
    default_code = 'unauthenticated'


class UserUnauthenticatedPost(APIException):
    status_code = 401
    default_detail = 'Unauthorized. Der Benutzer muss authentifiziert sein und ein Kundenprofil besitzen.'
    default_code = 'unauthenticated'


class UserHasAlreadyReview(APIException):
    status_code = 400
    default_detail = 'Fehlerhafte Anfrage. Der Benutzer hat möglicherweise bereits eine Bewertung für das gleiche Geschäftsprofil abgegeben.'
    default_code = 'forbidden'


class UserIsNotOwnerForDelete(APIException):
    status_code = 403
    default_detail = 'Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu löschen.'
    default_code = 'forbidden'


class UserIsNotConsumer(APIException):
    status_code = 403
    default_detail = 'Forbidden. Der Bentutzer ist kein typ vom Consumer.'
    default_code = 'forbidden'


class UserIsNotOwnerForPatch(APIException):
    status_code = 403
    default_detail = 'Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu bearbeiten.'
    default_code = 'forbidden'


class ReviewNotFound(APIException):
    status_code = 404
    default_detail = 'Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden.'
    default_code = 'not_found'


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Bad Request. Der Anfrage-Body enthält ungültige Daten.'
    default_code = 'bad_request'