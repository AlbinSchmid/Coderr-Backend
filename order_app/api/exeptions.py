from rest_framework.exceptions import APIException

class UserIsNotConsumer(APIException):
    status_code = 403
    default_detail = 'Benutzer hat keine Berechtigung, z.B. weil nicht vom typ customer.'
    default_code = 'false_user'

class OfferDetailNotExist(APIException):
    status_code = 404
    default_detail = 'Das angegebene Angebotsdetail wurde nicht gefunden.'
    default_code = 'not_found'