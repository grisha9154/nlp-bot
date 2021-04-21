import numpy as np

from nlp_module.normalize.normilize_text import get_normalize_tokens
from nlp_module.analyze.get_vector import get_vector
from nlp_module.temp_data.init_temp_data import tempData


def init_temp_vectors() -> None:
    vectors = list()
    temp_sentences = tempData.get_temp_list()
    for sentence in temp_sentences:
        tokens = get_normalize_tokens(sentence)
        if tokens is None:
            continue
        vector = get_vector(tokens)
        vectors.append(vector)

    temp_vectors = np.array(vectors)
    tempData.temp_vectors = temp_vectors

init_temp_vectors()
