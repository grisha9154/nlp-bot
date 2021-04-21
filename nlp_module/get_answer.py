from enum import Enum

from nlp_module.temp_data.data import GetTempIndexStatus
from nlp_module.temp_data.init_temp_data import get_temp_answer
from nlp_module.temp_data.get_temp_index import get_temp_index


class GetAnswerStatus(Enum):
    OK = 1
    UNKNOWN = 2
    UPDATE = 3


class GetAnswerResult:
    status: GetAnswerStatus = GetAnswerStatus.OK
    user_sentence: str = ''
    answer: str = None

    def __init__(self, user_sentence: str, status: GetAnswerStatus):
        self.user_sentence = user_sentence
        self.status = status


def get_user_answer(user_input: str) -> list[GetAnswerResult]:
    temp_index_result = get_temp_index(user_input)

    result_list = []

    for temp_result in temp_index_result:
        result_element = GetAnswerResult(temp_result.user_input, GetAnswerStatus(temp_result.status))
        if temp_result.status == GetTempIndexStatus.OK:
            answer = get_temp_answer(temp_result.temp_index)
            result_element.answer = answer
        result_list.append(result_element)

    return result_list
