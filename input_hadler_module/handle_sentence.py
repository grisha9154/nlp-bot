import re
import input_hadler_module.data as data_types

from nlp_module.analyze.data import GetUserVectorStatus
from nlp_module.analyze.get_user_vectors import get_user_vector
from nlp_module.normalize.normilize_text import get_normalize_tokens
from nlp_module.temp_data.data import GetTempIndexStatus
from nlp_module.temp_data.get_temp_index import get_index
from nlp_module.temp_data.init_temp_data import get_temp_answer


def handle_sentence(data: data_types.HandleSentenceData) -> None:
    if not append_normalize_tokens(data):
        return
    if not append_vector(data):
        return
    if not append_cos_dis(data):
        return
    if not append_answer(data):
        return

def append_normalize_tokens(data: data_types.HandleSentenceData) -> bool:
    normalize_tokens = get_normalize_tokens(data.sentence)
    if normalize_tokens is not None:
        data.normalize_tokens = normalize_tokens
        return True

    data.status = data_types.HandleSentenceStatus.EMPTY_INPUT
    return False


def append_vector(data: data_types.HandleSentenceData) -> bool:
    vector_handle_result = get_user_vector(list(data.normalize_tokens))
    if vector_handle_result.status is GetUserVectorStatus.OK.value:
        data.vector = vector_handle_result.user_vector
        return True

    data.status = data_types.HandleSentenceStatus.UNKNOWN
    return False


def append_cos_dis(data: data_types.HandleSentenceData) -> bool:
    temp_index_result = get_index(data.vector)
    if temp_index_result.status is GetTempIndexStatus.OK.value:
        data.index = temp_index_result.temp_index
        return True

    data.status = data_types.HandleSentenceStatus.UPDATE
    return False

def append_answer(data: data_types.HandleSentenceData) -> bool:
    patterns = '\\${(.*)}'
    answer = get_temp_answer(data.index)
    data.answer = answer
    matcher = re.findall(patterns, answer)
    if len(matcher) > 0:
        data.status = data_types.HandleSentenceStatus.NEED_MANAGER_ANSWER
    return True

