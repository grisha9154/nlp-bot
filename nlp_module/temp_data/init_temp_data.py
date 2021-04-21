import pandas as pd

from nlp_module.temp_data.get_vocab import get_vocab
from nlp_module.temp_data.temp_data import TempData

data_set_path = 'D:/projects/nlp-chat-bot/nlp-chat-bot-pyCharm/test-data/dialog_talk_agent_rus.xlsx'
df = pd.read_excel(data_set_path)
df.ffill(axis=0, inplace=True)

tempData = TempData(df)


def init_vocab() -> None:
    vocab = set(get_vocab(tempData.get_temp_list()))
    tempData.vocab = vocab


def get_temp_answer(temp_index: int) -> str:
    return tempData.df.loc[temp_index, 'Text Response']


init_vocab()
 