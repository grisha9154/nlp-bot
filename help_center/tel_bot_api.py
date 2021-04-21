from help_center.data import MessageHandlePayload
from help_center.addmin_worker import AdminWorker
from help_center.manager_worker import ManagerWorker
from input_hadler_module.input_handle import input_handle
import input_hadler_module.data as input_handler_data_type


class BotApi:
    bot_send_message = None
    message_map = dict()
    admin_map: dict[str, AdminWorker] = dict()
    manager_map: dict[str, ManagerWorker] = dict()

    def get_answer(self, sentences: list[input_handler_data_type.HandleSentenceData]) -> str:
        answers = [sentence.answer for sentence in sentences]
        return ' '.join(answers)

    def send_message(self, user_id: str, sentence: str):
        if self.bot_send_message:
            self.bot_send_message(user_id, sentence)
        else:
            print('Bot sender is not innit')

    def set_admin(self, admin_id):
        self.admin_map[admin_id] = AdminWorker(admin_id, admin_secret, self.bot_send_message, self.message_map)

    def set_manager(self, manager_id: str):
        self.manager_map[manager_id] = ManagerWorker(manager_id, manager_secret, self.bot_send_message, self.message_map)

    def send_unimproved_tokens(self, message: MessageHandlePayload):
        for admin_id in self.admin_map.keys():
            admin_work = self.admin_map.get(admin_id)
            admin_work.handle_unresolved_sentences(message)
        for manager_id in self.manager_map.keys():
            manager_worker = self.manager_map.get(manager_id)
            manager_worker.handle_unresolved_sentences(message)

    def init_bot_sender(self, bot_sender):
        self.bot_send_message = bot_sender

    def is_admin(self, user_id: str):
        return user_id in self.admin_map

    def is_manager(self, user_id: str):
        return user_id in self.manager_map

    def handle_message(self, message):
        if self.is_admin(message.from_user.id):
            admin_worker = self.admin_map.get(message.from_user.id)
            admin_worker.handle_message(message)
        elif self.is_manager(message.from_user.id):
            manager_worker = self.manager_map.get(message.from_user.id)
            manager_worker.handle_message(message)
        else:
            self.handle_user_message(message)

    def handle_user_message(self, message):
        user_id = message.from_user.id
        user_name = ' '.join([message.from_user.first_name, message.from_user.last_name])
        user_input = message.text

        handle_result = input_handle(user_input)
        if handle_result.is_answer_ready:
            answer = self.get_answer(handle_result.resolved_sentences)
            self.send_message(user_id, answer)
        else:
            payload = MessageHandlePayload(user_id, handle_result, user_name)
            self.message_map[payload.id] = payload
            self.send_unimproved_tokens(payload)


bot_api = BotApi()

admin_secret = '1'  # str(uuid4())
manager_secret = '1' # str(uuid4()
print('admin_secret: ', admin_secret)
print ('manager_secret: ', manager_secret)
