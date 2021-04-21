import numpy as np

from nlp_module.temp_data.init_temp_data import tempData


def get_vector(tokens: list[str]) -> np.ndarray:
    vocab_len = len(tempData.vocab)
    sorted_vocab = sorted(tempData.vocab)
    vector = np.zeros(vocab_len, dtype=int)

    for token in tokens:
        if token in tempData.vocab:
            vector[sorted_vocab.index(token)] = 1

    return vector
