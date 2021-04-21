import input_hadler_module.data as data_types

from input_hadler_module.handle_sentence import handle_sentence
from nlp_module.normalize.sentece_spliter import sentence_splitter


def input_handle(user_sentences) -> data_types.HandleInputData:
    sentences = sentence_splitter(user_sentences)
    handle_result = data_types.HandleInputData()

    for sentence in sentences:
        handle_sentence_data = data_types.HandleSentenceData(user_sentences, sentence)
        handle_sentence(handle_sentence_data)
        handle_result.resolved_sentences.append(handle_sentence_data)
        if handle_sentence_data.status != data_types.HandleSentenceStatus.OK:
            handle_result.unresolved_sentences.append(handle_sentence_data)
            handle_result.is_answer_ready = False
            handle_result.unresolved_sentences_dict[handle_sentence_data.id] = handle_sentence_data


    return handle_result
