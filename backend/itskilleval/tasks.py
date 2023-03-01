from celery import shared_task

from itskilleval.models.ai_model import AImodel
from itskilleval.models.eval import Eval
from itskilleval.models.job import Job
from itskilleval.service.models.ai_model_lightgbm import AiModelLightGBM
from itskilleval.service.pre_procession_data import PreProcessionData
from itskilleval.enum.eval_status import EvalStatus



@shared_task
def training(model_id):
    ai_model = AImodel.objects.get(pk=model_id)
    model = AiModelLightGBM(ai_model)
    model.train(model.get_model_file_path())

@shared_task
def predict(eval_id, model_id):

    try:
        eval = Eval.objects.get(id=eval_id)
        job = Job.objects.get(eval__id=eval_id)

        pre_procession_data = PreProcessionData(input_records=eval.input_value, model_id=model_id)
        normalization_data = pre_procession_data.pre_process_data()

        ai_model = AImodel.objects.get(id=model_id)
        model = AiModelLightGBM(ai_model)
        eval.result = model.predict(normalization_data)
        print(eval.result)
        eval.save()

        eval_status = EvalStatus.PREDICTED.value
    except Eval.DoesNotExist or Job.DoesNotExist as e:
        return False
    except Exception as e:
        job.detail = str(e)
        eval_status = EvalStatus.ERROR.value
    
    job.status = eval_status
    job.save()
    return True
