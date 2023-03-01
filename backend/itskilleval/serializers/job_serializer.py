from rest_framework import serializers

from itskilleval.models.job import Job

class JobSerializer(serializers.ModelSerializer):
    job_id = serializers.UUIDField(source='id')
    eval_id = serializers.UUIDField(source='eval.id')

    class Meta:
        model = Job
        fields = [
            'job_id',
            'eval_id',
        ]