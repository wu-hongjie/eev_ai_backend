
from itskilleval.models.job import Job

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class JobSearch(serializers.Serializer):
    id = serializers.UUIDField(required=True)

    class Meta:
        validators = []

    def validate_id(self, value):
        job = Job.objects.filter(id=value).first()
        if job is None:
            raise serializers.ValidationError(_('Job not found'), 404)

        return value