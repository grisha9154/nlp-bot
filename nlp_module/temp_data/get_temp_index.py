import numpy as np

from nlp_module.analyze.data import GetUserVectorStatus
from nlp_module.analyze.get_cosine_distance import get_cosine_distance
from nlp_module.analyze.get_user_vectors import get_user_vectors
from nlp_module.temp_data.data import GetTempIndexResult, GetTempIndexStatus
from nlp_module.temp_data.init_temp_data import tempData


def get_temp_index(user_input: str) -> list[GetTempIndexResult]:
    user_vectors_list = get_user_vectors(user_input)
    if len(user_vectors_list) == 0:
        return []
    temp_index = list()

    for user_vector in user_vectors_list:
        result_element = GetTempIndexResult(user_vector.user_sentence)
        if user_vector.status == GetUserVectorStatus.OK:
            get_index(user_vector.user_vector, result_element)
        else:
            result_element.status = GetTempIndexStatus.UNKNOWN
        temp_index.append(result_element)

    return temp_index


def get_index(vector: np.ndarray) -> GetTempIndexResult:
    result_element = GetTempIndexResult()
    cos_dis_list = get_cosine_distance(tempData.temp_vectors, np.array([vector])).flatten()
    min_value = min(cos_dis_list)
    if min_value > 0.3:
        result_element.status = GetTempIndexStatus.UPDATE
    else:
        index = cos_dis_list.tolist().index(min_value)
        result_element.temp_index = index

    return result_element
