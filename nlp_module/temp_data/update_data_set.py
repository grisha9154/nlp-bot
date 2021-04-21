import pandas as pd

from nlp_module.temp_data.get_temp_vector import init_temp_vectors
from nlp_module.temp_data.init_temp_data import tempData, data_set_path, init_vocab


def update_data_set(question, answer):
    df_list = tempData.df.values.tolist()
    df_list.append([question, answer])
    new_df = pd.DataFrame(df_list, columns=['Context', 'Text Response'])
    new_df.to_excel(data_set_path, index=False)
    tempData.df = new_df
    init_vocab()
    init_temp_vectors()
