from rest_framework.exceptions import APIException

class NoSellerUser(APIException):
    """
    Exception raised when the user is not a seller.
    """
    status_code = 403
    default_detail = 'Authentifizierter Benutzer ist kein business Profil.'
    default_code = 'no_business_user'

class OfferNotFound(APIException): 
    """
    Exception raised when the offer is not found.
    """
    status_code = 404
    default_detail = 'Das Angebot mit der angegebenen ID wurde nicht gefunden.'
    default_code = 'not_found'

class UserIsNotOwnerOffer(APIException):
    """
    Exception raised when the authenticated user is not the owner of the offer.
    """
    status_code = 403
    default_detail = "Authentifizierter Benutzer ist nicht der Eigentümer des Angebots."
    default_code = "not_found"

class IncorrectParams(APIException):
    """
    Exception raised when the request parameters are incorrect.
    """
    status_code = 400
    default_detail = "Ungültige Anfrageparameter."
    default_code = "bad_request"

class BadRequest(APIException):
    """
    Exception raised when the request is invalid or incomplete.
    """
    status_code = 400
    default_detail = "Ungültige Anfragedaten oder unvollständige Details."
    default_code = "bad_request"