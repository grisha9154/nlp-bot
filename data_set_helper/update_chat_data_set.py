from data_set_helper.instagram.get_inst_messages_data import get_inst_messages_data
from data_set_helper.save_to_excel import save_pairs_to_excel

switcher = {
    'inst': get_inst_messages_data
}


def update_chat_data_set(source_type, current_user_name):
    source_getter = switcher[source_type]
    pairs = source_getter(current_user_name)
    save_pairs_to_excel(pairs)


update_chat_data_set('inst', 'ФОТОГРАФ МИНСК')
