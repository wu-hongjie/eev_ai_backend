from django.db import models
import uuid
import json

from accounts.models.user import User
from .ai_model import AImodel

from itskilleval.enum.input_type import InputType
from django.utils.translation import gettext_lazy as _

class AImodelInput(models.Model):
    INPUT_TYPE = (
        (0, _('input number')),
        (1, _('input category'))
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aimodel = models.ForeignKey(AImodel, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=256, null=False, blank=False)
    type = models.PositiveSmallIntegerField(choices=INPUT_TYPE, blank=False, null=True, default=0)
    min = models.FloatField(blank=True, null=True, default=0)
    max = models.FloatField(blank=True, null=True, default=0)
    category = models.JSONField(max_length=1024, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='aimodel_input_updated_by')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='aimodel_input_created_by')

    class Meta:
        db_table = 'aimodel_inputs'
        verbose_name = _('AI model input')
        verbose_name_plural = _('AI model inputs')

    def subMaxMin(self):
        return (self.max - self.min) if self.isType(InputType.NUMERIC.value) else None

    def isType(self, type = InputType.NUMERIC.value):
        return self.type == type
    
    def getLenItemsCategory(self):
        return len(self.category)
    
    def findIdOfItemCategory(self, value):
        id = None
        for item in self.category:
            if item['value'] == value:
                id = item['id']
                break
        
        return id
