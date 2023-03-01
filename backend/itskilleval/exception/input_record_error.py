
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
class InputRecordError(APIException):
    """ Input record from client is invalid"""

    status_code = 400
    default_detail = _("Invalid input")
    default_code = _("Bad request")