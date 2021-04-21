import numpy as np

from nlp_module.analyze.data import GetUserVectorResult, GetUserVectorStatus
from nlp_module.analyze.get_vector import get_vector
from nlp_module.normalize.normilize_text import get_normalize_tokens
from nlp_module.normalize.sentece_spliter import sentence_splitter


def get_user_vectors(user_input: str) -> list[GetUserVectorResult]:
    user_sentences = sentence_splitter(user_input)

    vectors_list = list()

    for sentence in user_sentences:
        result_item = GetUserVectorResult(sentence)
        normalize_tokens = list(get_normalize_tokens(sentence))
        if normalize_tokens is None:
            continue
        user_vector = get_vector(normalize_tokens)
        vector_len = np.linalg.norm(user_vector)
        if vector_len == 0:
            result_item.status = GetUserVectorStatus.UNKNOWN
        else:
            result_item.user_vector = user_vector
        vectors_list.append(result_item)

    return vectors_list


def get_user_vector(normalize_tokens: list[str]) -> GetUserVectorResult:
    result_item = GetUserVectorResult('')
    user_vector = get_vector(normalize_tokens)
    vector_len = np.linalg.norm(user_vector)
    if vector_len == 0:
        result_item.status = GetUserVectorStatus.UNKNOWN
    else:
        result_item.user_vector = user_vector

    return result_item
