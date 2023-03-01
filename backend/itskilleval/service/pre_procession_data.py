
from itskilleval.models.ai_model_input import AImodelInput
from itskilleval.enum.input_type import InputType
from itskilleval.exception.input_record_error import InputRecordError

import json
import numpy as np
from django.utils.translation import gettext_lazy as _

# Processing
class PreProcessionData:

    def __init__(self, input_records, model_id):
        self.input_records = input_records
        self.model_id = model_id

    def pre_process_data(self):
        normalized_data_arr = []

        for items in self.input_records:
            normalized_data_arr_item = []
            aimodel_input_names = list(items.keys())
            aimodel_input_names.remove('id')

            aimodel_inputs = AImodelInput.objects.filter(
                aimodel_id = self.model_id
            ).order_by('name')

            if len(aimodel_input_names) != len(aimodel_inputs):
                raise InputRecordError(_("Input length is wrong"))

            for aimodel_input in aimodel_inputs:
                if(aimodel_input.name not in items):
                    raise InputRecordError(aimodel_input.name + _(" was not found"))

                normalized_data = self.__normalize_data(float(items[aimodel_input.name]), aimodel_input)
                if normalized_data is None:
                    raise InputRecordError(_("Normalize error"))

                normalized_data_arr_item.append(normalized_data)

            input = self.__combine_input(normalized_data_arr_item)

            normalized_data_arr.append(input)

        return normalized_data_arr


    def __normalize_data(self, value, aimodel_input):
        normalized_data = []

        if aimodel_input.isType(InputType.NUMERIC.value):
            normalized_data = self.__normalize_numeric_data(value=value, aimodel_input=aimodel_input)
        elif aimodel_input.isType(InputType.CATEGORY.value):
            normalized_data = self.__normalize_category_data()
        
        return normalized_data

    def __normalize_category_data(self, value, aimodel_input):
        len_category = aimodel_input.getLenItemsCategory()
        id = aimodel_input.findIdOfItemCategory(value)

        if (len_category == 0) or (id is None):
            return None
        
        return np.eye(1, len, id)

    def __normalize_numeric_data(self, value, aimodel_input):
        subMaxMin = aimodel_input.subMaxMin()
        if (subMaxMin == 0) or (subMaxMin is None):
            return None

        return [(value - aimodel_input.min)/subMaxMin]

    def __combine_input(self, normalized_data_arr):
        return np.hstack(normalized_data_arr) if len(normalized_data_arr) > 0 else []
