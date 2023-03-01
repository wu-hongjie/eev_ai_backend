from itskilleval.models.eval import Eval

from rest_framework import serializers

class EvalSerializer(serializers.ModelSerializer):
    eval_id = serializers.UUIDField(source='id')
    
    class Meta:
        model = Eval
        fields = [
            'eval_id',
            'system_id',
            'result',
            'updated_at'
        ]
