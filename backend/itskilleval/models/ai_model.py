from django.db import models
from accounts.models.user import User
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os

def train_data_path(instance, file_name):
    return '{}/{}/{}'.format(os.environ.get('TRAINING_DIR'), instance.id, file_name)

class AImodel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32, null=False, blank=False)
    output_amount = models.PositiveIntegerField(null=False, blank=False)
    training_file = models.FileField(upload_to=train_data_path, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='aimodel_updated_by')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='aimodel_created_by')

    class Meta:
        db_table = 'aimodels'
        verbose_name = _('AI model')
        verbose_name_plural = _('AI models')

    def __str__(self):
        return self.name
    