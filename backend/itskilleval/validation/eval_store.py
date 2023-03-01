from rest_framework import serializers
from itskilleval.models.ai_model import AImodel
import os
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class EvalStore(serializers.Serializer):

    aimodel_id = serializers.UUIDField(required=True)
    system_id = serializers.CharField(required=True, max_length=128, allow_blank=False)
    input_records = serializers.JSONField(required=True, allow_null=False)

    class Meta:
        validator = []


    def validate_input_records(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(_("Records is invalid"), 403)

        is_valid = True
        for item in value:
            if not item:
                is_valid = False
                break

            if 'id' not in item:
                is_valid = False
                break
            
            if len(item) == 1:
                is_valid = False
                break
            
            for key in item:
                try:
                    float(item[key])
                except Exception:
                    is_valid = False
                    break

        if not is_valid:
            raise serializers.ValidationError(_("Records is invalid"), 403)
            
        return value
    
    def validate_aimodel_id(self, value):
        is_valid = True
        msg = []
        if not value:
            raise serializers.ValidationError(_("Ai model not found"), 404)
        
        # Throw exception if aimodel not found
        ai_model = AImodel.objects.filter(id=value).first()

        if ai_model is None:
            raise serializers.ValidationError(_("Ai model not found"), 404)
        
        dir_path = os.path.join(settings.MEDIA_ROOT, os.environ.get('MODEL_DIR'))
        model_file_path = "{}/{}.pb".format(dir_path, str(value))
        if os.path.exists(model_file_path) is False:
            raise serializers.ValidationError(_("Ai model not found"), 404)

        return value

