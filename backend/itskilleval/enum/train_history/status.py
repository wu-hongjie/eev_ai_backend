from enum import Enum
from django.utils.translation import gettext_lazy as _

class Status(Enum):
    NOT_TRAIN   = _("Model was not trained")
    NOT_UPDATE  = _("Model was not updated")
    UPDATED     = _("Model was updated")
