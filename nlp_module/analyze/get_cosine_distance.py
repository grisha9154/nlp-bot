import numpy as np
from scipy.spatial.distance import cdist


def get_cosine_distance(chat_template_vector_stack: np.ndarray, user_input_vector: np.ndarray) -> np.ndarray:
    cos_dis_list = cdist(chat_template_vector_stack, user_input_vector, metric='cosine')
    return cos_dis_list
