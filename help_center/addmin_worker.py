import help_center.data as help_center_data_type
import input_hadler_module.data as input_handler_data_type

from help_center.worker import Worker
from nlp_module.normalize.normilize_text import get_normalize_tokens
from nlp_module.temp_data.update_data_set import update_data_set

message_answer_sep = '|'

class AdminWorker(Worker):
    def __init__(self, worker_id: str, secret: str, sender, messages):
        Worker.__init__(self, worker_id, secret, sender, messages)

    def handle_unresolved_sentences(self, handle_payload: help_center_data_type.MessageHandlePayload):
        unresolved_sentences = handle_payload.payload.unresolved_sentences
        for unresolved_sentence in unresolved_sentences:
            if unresolved_sentence.status.value == input_handler_data_type.HandleSentenceStatus.UNKNOWN.value or unresolved_sentence.status.value == input_handler_data_type.HandleSentenceStatus.EMPTY_INPUT.value or unresolved_sentence.status.value == input_handler_data_type.HandleSentenceStatus.UPDATE.value :
                sentence_id = unresolved_sentence.id
                self.send_to_worker(sentence_id)
                self.send_to_worker(unresolved_sentence.context)
                self.send_to_worker(unresolved_sentence.sentence)

    def handle_action(self, action_type: str, value: str):
        if action_type == 'a':
            self.handle_update_data(value)
            return

    def handle_update_data(self, value: str):
        answer_parts = value.split(message_answer_sep)
        sentence_id = answer_parts[0]
        answer = answer_parts[1]
        message_to_answer = self.get_message_to_answer(sentence_id)
        sentence = message_to_answer.payload.unresolved_sentences_dict.get(sentence_id)
        if not message_to_answer:
            self.send_to_worker('Wrong Message Id')
        else:
            normalize_tokens = get_normalize_tokens(sentence.sentence)
            if normalize_tokens is None:
                question = 'пустой'
            else:
                question = ' '.join(get_normalize_tokens(sentence.sentence))
            update_data_set(question, answer)

            self.send_to_worker('Data is updated')

            self.send_confirm_answer(message_to_answer, answer, sentence_id)


