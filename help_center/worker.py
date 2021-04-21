import help_center.data as help_center_data_type
import input_hadler_module.data as input_handler_data_type

type_sep = '::'

class Worker:
    def __init__(self, id: str, secret: str, sender, messages):
        self.id = id
        self.secret = secret
        self.sender = sender
        self.is_confirm = False
        self.messages_map = messages

    def confirm(self):
        self.is_confirm = True

    def send_to_user(self, user_id: str, text: str):
        self.sender(user_id, text)

    def send_to_worker(self, text: str):
        self.sender(self.id, text)

    def send_reject_message(self):
        self.send_to_worker('Nope')

    def confirm_account(self, secret: str):
        if self.secret == secret:
            self.confirm()
            self.send_to_worker('Confirm successes')
            return
        else:
            self.send_reject_message()
            return

    def handle_message(self, message):
        message_parts = message.text.split(type_sep)
        action_type = str(message_parts[0]).lower()
        value = message_parts[1]

        if action_type == 'c':
            self.confirm_account(value)
            return

        if not self.is_confirm:
            self.send_reject_message()
            return

        self.handle_action(action_type, value)

    def send_confirm_answer(self, message_to_answer, answer, sentence_id):
        if self.update_message(message_to_answer, answer, sentence_id):
            answer_to_send = self.get_answer_to_send(message_to_answer)
            self.send_to_user(message_to_answer.user_id, answer_to_send)
            self.send_to_worker('Answer is send')

    def update_message(
            self,
            message: help_center_data_type.MessageHandlePayload,
            answer: str,
            sentence_id: str,
    ) -> bool:
        sentence = message.payload.unresolved_sentences_dict[sentence_id]
        sentence.answer = answer
        sentence.status = input_handler_data_type.HandleSentenceStatus.OK
        sentences_ready_status = True
        for resolved_sentence in message.payload.resolved_sentences:
            if resolved_sentence.status.value != input_handler_data_type.HandleSentenceStatus.OK.value:
                sentences_ready_status = False
                break

        return sentences_ready_status

    def get_answer_to_send(self, message: help_center_data_type.MessageHandlePayload) -> str:
        return ' '.join(sentence.answer for sentence in message.payload.resolved_sentences)

    def get_message_to_answer(self, sentence_id: str) -> help_center_data_type.MessageHandlePayload or None:
        for message in self.messages_map.values():
            sentence = message.payload.unresolved_sentences_dict.get(sentence_id)
            if sentence:
                return message

    def handle_action(self, action_type: str, value: str):
        pass
