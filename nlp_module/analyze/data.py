import numpy as np

from enum import Enum


class GetUserVectorStatus(Enum):
    OK = 1
    UNKNOWN = 2


class GetUserVectorResult:
    status: GetUserVectorStatus = 1
    user_sentence = ''
    user_vector: np.ndarray = None
    def __init__(self, user_sentence):
        self.user_sentence = user_sentence
