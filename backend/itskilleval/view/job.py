from itskilleval.validation.job_search import JobSearch
from itskilleval.models.job import Job
from rest_framework.response import Response

from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication

class JobView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, job_id):
        data = request.query_params.dict()
        data['id'] = job_id
        
        validation_data = JobSearch(data=data)
        validation_data.is_valid(raise_exception=True)
        
        validated_data = validation_data.validated_data
        job = Job.objects.filter(
            id=validated_data['id']
        ).first()
        
        data = {
            "eval_id": job.eval.id,
            "job_status": job.status,
            "job_detail": job.detail
        }
        
        return Response(data=data)
        