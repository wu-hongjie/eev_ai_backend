from django.db import models
from accounts.models.user import User
from .ai_model import AImodel
import uuid
from django.utils.translation import gettext_lazy as _
import json

class Eval(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aimodel = models.ForeignKey(AImodel, on_delete=models.CASCADE, null=False, related_name='aimodel_id')
    system_id = models.CharField(max_length=128, null=False, blank=False)
    input_value = models.JSONField(max_length=2048, null=False, blank=False)
    result = models.JSONField(max_length=1024, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'evals'
        verbose_name = _('Eval')
        verbose_name_plural = _('Evals')

    def save(self, *args, **kwargs):
        if self.result is not None:
            self.__convert_result_to_json()
        return super().save(*args, **kwargs)
    
    def __convert_result_to_json(self):
        if(self.__is_json(self.result)):
            return self.result
        results = []
        index = 0
        for item in self.input_value:
            result = {
                'id': item['id'],
                'result': list(self.result[index])
            }
            index += 1
            results.append(result)
        self.result = json.dumps(results)
        return self.result

    def __is_json(self, val):
        try:
            json.loads(val)
        except Exception as e:
            return False
        return True