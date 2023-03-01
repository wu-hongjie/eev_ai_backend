from rest_framework import serializers
from itskilleval.models.eval import Eval
from itskilleval.models.ai_model import AImodel

from django.utils.translation import gettext_lazy as _
import time

class EvalSearch(serializers.Serializer):
    aimodel_id = serializers.UUIDField(required=True)
    system_id = serializers.CharField(required=True, max_length=128, allow_blank=False)
    eval_id = serializers.CharField(required=False, max_length=128, allow_blank=False)
    from_date = serializers.DateField(required=False, allow_null=False)
    to_date = serializers.DateField(required=False, allow_null=False)

    class Meta:
        validators = []

    def validate_aimodel_id(self, value):
        if not value:
            raise serializers.ValidationError(_("Ai model not found"), 404)

        # Throw exception if aimodel not found
        ai_model = AImodel.objects.filter(id = value).first()
        if ai_model is None:
            raise serializers.ValidationError(_("Ai model not found"), 404)

        return value
    
    def validate_eval_id(self, value):
        eval = Eval.objects.filter(id=value).first()
        if eval is None:
            raise serializers.ValidationError(_("Eval model not found"), 404)
            
        return value
    
    def validate_to_date(self, value):
        if self.initial_data['to_date'] < self.initial_data['from_date']:
            raise serializers.ValidationError(_("To date must great than or equal from date"))
        
        return value