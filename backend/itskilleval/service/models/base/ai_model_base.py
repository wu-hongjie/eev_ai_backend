import os
from django.conf import settings

import itskilleval.models.ai_model
import itskilleval.models.ai_model_input
import itskilleval.models.train_history
import itskilleval.models.eval

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from django.utils.translation import gettext_lazy as _


class AiModelBase():

    loaded_models = {}

    # Todo: using dependency injection to init ai_model
    def __init__(self, ai_model):
        
        self.ai_model = ai_model
        self.model = None

        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None

        self.X_test = None
        self.y_test = None

        self.test_size = float(os.environ.get('TRAINING_DATA_TEST_RATIO'))
        self.X_test = None
        self.y_test = None

        self.y_pred = None

        self.retrain_data = []

        self.retrain_data_count = {}
    
    def save_model(self):
        pass

    def save_params(self):
        pass
    
    def get_model_file_path(self):
        dir_path = os.path.join(settings.MEDIA_ROOT, os.environ.get('MODEL_DIR'))
        path = "{}/{}.pb".format(dir_path, str(self.ai_model.id))
        return path

    def get_param_file_path(self):
        dir_path = os.path.join(settings.MEDIA_ROOT, 'models', 'params')
        path = "{}/{}.params".format(dir_path, str(self.ai_model.id))
        return path

    def get_train_data_file_path(self):
        path = self.ai_model.training_file.path
        if os.path.exists(path=path) is False:
            raise FileNotFoundError(_("File not found"))
        return path

    def get_pred_data_file_path(self):
        dir_path = os.path.join(settings.MEDIA_ROOT, 'train_data')
        path = "{}/pred_data.csv".format(dir_path)
        if os.path.exists(path=path) is False:
            raise FileNotFoundError(_("File not found"))
        return path


    def load_model(self, model_file_path):
        pass

    def load_data(self):
        train_data_file_path = self.get_train_data_file_path()

        data = pd.read_csv(train_data_file_path)

        self.y = data.iloc[:, 0:self.ai_model.output_amount]
        self.X = data.iloc[:, self.ai_model.output_amount:]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.y,
            test_size=self.test_size,
            shuffle=False
        )

    def train(self, model_file_path=None):

        self.load_model(model_file_path)

        self.load_data()

    def predict(self, data):
        self.load_model(self.get_model_file_path())
        self.y_pred = self.model.predict(data)
        return self.y_pred
