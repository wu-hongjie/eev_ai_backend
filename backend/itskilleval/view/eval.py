from rest_framework.views import APIView
from rest_framework.response import Response
from itskilleval.validation.eval_search import EvalSearch
from itskilleval.validation.eval_store import EvalStore
from itskilleval.serializers.eval_serializer import EvalSerializer
from itskilleval.serializers.job_serializer import JobSerializer
from itskilleval.models.eval import Eval
from itskilleval.models.ai_model import AImodel
from itskilleval.service.pre_procession_data import PreProcessionData
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.pagination import PageNumberPagination
from itskilleval.service.models.ai_model_lightgbm import AiModelLightGBM
from itskilleval.models.job import Job
from itskilleval.enum.eval_status import EvalStatus
from itskilleval.tasks import predict
import os
from datetime import datetime, time

class EvalView(APIView, PageNumberPagination):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]
    page_size = os.environ.get('PAGE_SIZE')
        
    def get(self, request, model_id):
        requestData = request.query_params.dict()

        requestData['aimodel_id'] = model_id
        validation = EvalSearch(data=requestData)

        validation.is_valid(raise_exception=True)
        validated_data = validation.validated_data

        evals = Eval.objects.filter(
            aimodel__id = model_id,
            system_id = validated_data['system_id'],
        )
        
        if 'eval_id' in requestData and validated_data['eval_id']:
            evals = evals.filter(id=validated_data['eval_id'])
        if 'from_date' in requestData and validated_data['from_date']:
            # combine to make min datetime with time 00:00:00
            evals = evals.filter(updated_at__gte=datetime.combine(validated_data['from_date'], time.min))
        if 'to_date' in requestData and validated_data['to_date']:
            # combine to make max datetime with time 23:59:59
            evals = evals.filter(updated_at__lte=datetime.combine(validated_data['to_date'], time.max))

        result = self.paginate_queryset(evals, request, view=self)
        dataSerializer = EvalSerializer(result, many=True)

        return self.get_paginated_response(dataSerializer.data)

    # Processing
    def post(self, request, model_id):
        data = request.data
        data['aimodel_id'] = model_id

        validation = EvalStore(data=data)
        validation.is_valid(raise_exception=True)
        data = validation.validated_data
        
        eval = Eval(
            aimodel_id=model_id,
            system_id=data['system_id'],
            input_value=data['input_records'],
        )
        eval.save()
        
        job = Job(
            eval=eval,
            status = EvalStatus.PREDICTING.value
        )
        job.save()

        predict.delay(eval_id=eval.id, model_id=model_id)

        jobSerializer = JobSerializer(job)

        return Response(data=jobSerializer.data)
