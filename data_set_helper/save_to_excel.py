import pandas as pd
from uuid import uuid4

from nlp_helper.normalize.normilize_text import get_normalize_text

excel_directory_path = 'D:/projects/nlp-chat-bot/nlp-chat-bot-pyCharm/data-set'
excel_file_path = '/dialog_talk_agent_rus'
excel_extension = '.xlsx'


def save_pairs_to_excel(pairs):
    contexts = []
    response = []
    for pair in pairs:
        normalize_question = get_normalize_text(pair.question)
        if normalize_question == '':
            continue
        contexts.append(normalize_question)
        response.append(pair.answer)

    df = pd.DataFrame({
        'Context': contexts,
        'Text Response': response,
    })
    df.to_excel(get_excel_file_name(), index=False)


def get_excel_file_name():
    excel_id = uuid4()
    return excel_directory_path + excel_file_path + '_' + str(excel_id) + excel_extension
