from enum import Enum

class EvalStatus(Enum):
    PREDICTING = 1
    PREDICTED = 2
    ERROR = 3