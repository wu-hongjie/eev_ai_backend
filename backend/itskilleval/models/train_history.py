from django.db import models
from accounts.models.user import User
from .ai_model import AImodel
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

class TrainHistory(models.Model):
    REPLACED_MODEL = (
        (0, _('no aimodel updated')),
        (1, _('aimodel updated'))
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aimodel = models.ForeignKey(AImodel, on_delete=models.CASCADE, null=False)
    training_count = models.PositiveIntegerField(null=False, blank=False, default=0)
    accuracy = models.FloatField(null=False, blank=False, default=0)
    loss = models.FloatField(null=False, blank=False, default=0)
    replaced_model = models.PositiveSmallIntegerField(choices=REPLACED_MODEL, default=0)
    status = models.CharField(max_length=128, null=True, blank=True)
    started_date = models.DateTimeField()
    ended_date = models.DateTimeField(default=now)

    class Meta:
        db_table = 'train_histories'
        verbose_name = _('Train history')
        verbose_name_plural = _('Train histories')