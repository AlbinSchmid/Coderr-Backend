from rest_framework.exceptions import APIException

class UserIsNotConsumer(APIException):
    """
    Exception raised when the user is not a consumer.
    """
    status_code = 403
    default_detail = 'Benutzer hat keine Berechtigung, z.B. weil nicht vom typ customer.'
    default_code = 'false_user'

class UserIsNotSeller(APIException):
    """
    Exception raised when the user is not a seller.
    """
    status_code = 403
    default_detail = 'Benutzer hat keine Berechtigung, diese Bestellung zu aktualisieren.'
    default_code = 'false_user'

class UserIsNotStaff(APIException):
    """
    Exception raised when the user is not a staff member.
    """
    status_code = 403
    default_detail = 'Benutzer hat keine Berechtigung, die Bestellung zu löschen.'
    default_code = 'false_user'

class UserSellerNotFound(APIException):
    """
    Exception raised when the seller user is not found.
    """
    status_code = 404
    default_detail = 'Kein Geschäftsnutzer mit der angegebenen ID gefunden.'
    default_code = 'not_found'

class OfferDetailNotExist(APIException):
    """
    Exception raised when the offer detail does not exist.
    """
    status_code = 404
    default_detail = 'Das angegebene Angebotsdetail wurde nicht gefunden.'
    default_code = 'not_found'

class OrderNotFound(APIException):
    """
    Exception raised when the order is not found.
    """
    status_code = 404
    default_detail = 'Die angegebene Bestellung wurde nicht gefunden.'
    default_code = 'not_found'

class IncorrectStatus(APIException):
    """
    Exception raised when the status is incorrect.
    """
    status_code = 400
    default_detail = 'Ungültiger Status oder unzulässige Felder in der Anfrage.'
    default_code = 'bad_request'


