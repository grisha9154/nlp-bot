from bs4 import BeautifulSoup

from data_set_helper.data.question_answer_pair import QuestionAnswerPair
from data_set_helper.instagram.get_inst_data_set import get_data_set
from data_set_helper.map_to_question_annotation_pairs import map_to_question_answer_pair

folderPath = 'D:/projects/nlp-chat-bot/lowa.card_20210411/'
path = folderPath + '/messages/chats.html'


file = open(path, mode='r', encoding='utf8')
fileData = file.read()


def get_inst_messages_data(current_user_name):
    soup = BeautifulSoup(fileData, features='lxml')
    main_div = soup.find('div', {'role': 'main'})
    chats_container_div = main_div.find_all('div', {'class': '_2lek'})
    messages_info_list = []
    for chatDiv in chats_container_div:
        link = chatDiv.find('a', href=True)
        chat_file = open(folderPath+link['href'], 'r', encoding='utf8')
        chat_file_text = chat_file.read()
        chat_info = get_data_set(chat_file_text, current_user_name)
        pairs = map_to_question_answer_pair(chat_info)
        pairs.append(QuestionAnswerPair())
        messages_info_list.extend(pairs)
    return messages_info_list
