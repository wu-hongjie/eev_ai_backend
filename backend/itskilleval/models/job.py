from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

from accounts.models.user import User
from .eval import Eval

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=False)
    status = models.PositiveSmallIntegerField()
    detail = models.CharField(max_length=512, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='job_updated_by')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='job_created_by')

    class Meta:
        db_table = 'jobs'
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')