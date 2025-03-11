from rest_framework.exceptions import APIException

class UserIsNotConsumer(APIException):
    status_code = 403
    default_detail = 'Benutzer hat keine Berechtigung, z.B. weil nicht vom typ customer.'
    default_code = 'false_user'

class UserIsNotSeller(APIException):
    status_code = 403
    default_detail = 'Benutzer hat keine Berechtigung, diese Bestellung zu aktualisieren.'
    default_code = 'false_user'

class UserIsNotStaff(APIException):
    status_code = 403
    default_detail = 'Benutzer hat keine Berechtigung, die Bestellung zu löschen.'
    default_code = 'false_user'

class OfferDetailNotExist(APIException):
    status_code = 404
    default_detail = 'Das angegebene Angebotsdetail wurde nicht gefunden.'
    default_code = 'not_found'

class OrderNotFound(APIException):
    status_code = 404
    default_detail = 'Die angegebene Bestellung wurde nicht gefunden.'
    default_code = 'not_found'

