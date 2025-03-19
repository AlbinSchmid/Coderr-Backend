from rest_framework.exceptions import APIException

class NoSellerUser(APIException):
    status_code = 403
    default_detail = 'Authentifizierter Benutzer ist kein business Profil.'
    default_code = 'no_business_user'

class OfferNotFound(APIException):
    status_code = 404
    default_detail = 'Das Angebot mit der angegebenen ID wurde nicht gefunden.'
    default_code = 'not_found'

class UserIsNotOwnerOffer(APIException):
    status_code = 403
    default_detail = "Authentifizierter Benutzer ist nicht der Eigentümer des Angebots."
    default_code = "not_found"

class IncorrectParams(APIException):
    status_code = 400
    default_detail = "Ungültige Anfrageparameter."
    default_code = "bad_request"

class BadRequest(APIException):
    status_code = 400
    default_detail = "Ungültige Anfragedaten oder unvollständige Details."
    default_code = "bad_request"