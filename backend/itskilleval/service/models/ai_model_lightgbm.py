import os

from itskilleval.service.models.base.ai_model_base import AiModelBase
from itskilleval.models.train_history import TrainHistory
from itskilleval.enum.train_history.replaced_model import ReplaceModel as TrainHistoryReplaceModel
from itskilleval.enum.train_history.status import Status as TrainHistoryStatus

from django.db import transaction
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
import lightgbm as lgb
import pickle
import numpy as np
from django.utils.timezone import now

class AiModelLightGBM(AiModelBase):

    def __init__(self, ai_model):
        super().__init__(ai_model)

        self.params = {
            'objective': 'regression',
            'metric': 'l2',
            'num_leaves': 2,
            'verbosity': -1
        }

        self.lgb_train = None

        self.lgb_test = None
    
    def load_model(self, model_file_path):
        if model_file_path is not None and os.path.isfile(model_file_path):
            with open(model_file_path, 'rb') as file:
                self.model = pickle.load(file)
        else:
            self.model = MultiOutputRegressor(lgb.LGBMRegressor(**self.params))

    def load_data(self):
        super().load_data()

        self.lgb_train = lgb.Dataset(self.X_train, self.y_train)
        self.lgb_test = lgb.Dataset(self.X_test, self.y_test, reference=self.lgb_train)
    
    def save_model(self):
        model_file_path = self.get_model_file_path()
        with open(model_file_path, 'wb+') as file:
            pickle.dump(self.model, file)
    
    def save_params(self):
        return super().save_params()
    
    def load_params(self):
        params_file_path = self.get_param_file_path()
        if os.path.isfile(params_file_path):
            with open(params_file_path, 'rb') as file:
                self.params = pickle.load(file)
            
            self.params['objective'] = 'regression'
            self.params['metric'] = 'l2'
    
    def train(self, model_file_path=None):
        if TrainHistory.objects.filter(aimodel=self.ai_model).order_by('loss').exists():
            last_train_history = TrainHistory.objects.filter(aimodel=self.ai_model).order_by('loss')[0]
            training_count = TrainHistory.objects.filter(aimodel=self.ai_model).count() + 1
            last_loss = last_train_history.loss
        else:
            training_count = 1
            last_loss = 1.0

        replaced_model = TrainHistoryReplaceModel.NO.value
        status = TrainHistoryStatus.NOT_TRAIN.value
        current_lost = 1.0
        accuracy = 0.0
        started_date = now()

        try:
            self.load_params()

            #親のAIModelBaseクラスでモデル・学習データの読み込みを行う
            super().train(model_file_path)

            print(' ------ Start training ------')
            self.model.fit(self.X_train, self.y_train)
            print(' ------ Finish training ------')

            print('Model Name: {}'.format(self.ai_model.name))

            # evaluation
            self.y_pred = self.model.predict(self.X_test)

            # calculate RMSE
            mse = mean_squared_error(self.y_test, self.y_pred)
            rmse = np.float(np.sqrt(mse))
            current_lost = rmse

            # calculate accuracy
            accuracy = r2_score(self.y_test, self.y_pred)
            
            if rmse < last_loss:
                replaced_model = TrainHistoryReplaceModel.YES.value
                status = TrainHistoryStatus.UPDATED.value
                self.save_model()
            else:
                status = TrainHistoryStatus.NOT_UPDATE.value
        except FileNotFoundError as e:
            print('lightGBM train error:', e)
        except Exception as e:
            print('lightGBM train error:', e)
        finally:
            train_history = TrainHistory(
                aimodel=self.ai_model,
                training_count=training_count,
                replaced_model=replaced_model,
                status=status,
                accuracy=accuracy,
                loss=current_lost,
                started_date=started_date
            )

            train_history.save()
