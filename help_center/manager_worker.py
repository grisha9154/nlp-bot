import re
import help_center.data as help_center_data_type

from help_center.worker import Worker
from input_hadler_module.data import HandleSentenceStatus

correct_date = '${correct_date}'
package_ind = '${package_ind}'
package_love = '${package_love}'
package_family = '${package_family}'
deal_confirm = '${deal_confirm}'
package_answer = {
    '${package_ind}': 'Индивидуальный портрет \n' \
                     'Фотосъёмка о человеке, личности. Если вы не можете определиться с тем, ' \
                     'какую фотосъёмку вы себе хотите, но внутреннее желание есть, посмотрите мои работы.' \
                     'Что вам нравится? Цвета, композиция или образ, в котором вы себя можете увидеть. \n' \
                     'Если вы, искренне, не можете ответить на этот вопрос, то напишите мне, мы с вами индивидуально продумаем все ' \
                     'моменты. \n' \
                     '1. Стоимость 250 byn\n' \
                     '2. 15 фото в ретуши и цветокоррекции\n' \
                     '3. Исходных фотографий в цветокоррекции от 100 штук\n' \
                     '4. Аренда фотостудии, макияж, мастер по причёскам, в эту стоимость не входят\n' \
                     '5. Готовая работа до 8 дней\n',
    '${package_love}': '\n'.join([
        'Love story или семейная',
        'Я не говорю, «как вам встать», а направляю ваши действия, всё Позирование происходит естественным образом, потому что всё ваше внимание сконцентрировано только друг на друге',
        '1. Стоимость 300 byn',
        '2. 15 фото в ретуши и цветокоррекции',
        '3. Исходных фотографий в цветокоррекции от 100 штук',
        '4. Аренда фотостудии, макияж, мастер по причёскам, в эту стоимость не входят',
        '5. Готовая работа до 8 дней',
        ]),
    '${package_family}': '\n'.join([
        'Love story или семейная',
        'Я не говорю, «как вам встать», а направляю ваши действия, всё Позирование происходит естественным образом, потому что всё ваше внимание сконцентрировано только друг на друге',
        '1. Стоимость 300 byn',
        '2. 15 фото в ретуши и цветокоррекции',
        '3. Исходных фотографий в цветокоррекции от 100 штук',
        '4. Аренда фотостудии, макияж, мастер по причёскам, в эту стоимость не входят',
        '5. Готовая работа до 8 дней',
        ]),
}

patterns = '\\${.*}'
message_answer_sep = '|'

class ManagerWorker(Worker):
    def __init__(self, id: str, secret: str, sender, messages):
        Worker.__init__(self, id, secret, sender, messages)

    def handle_action(self, action_type: str, value: str):
        if action_type == 'cor':
            self.handle_correct_date_action(value)

    def handle_correct_date_action(self, value: str):
        answer_parts = value.split(message_answer_sep)
        sentence_id = answer_parts[0]
        message_to_answer = self.get_message_to_answer(sentence_id)
        sentence = message_to_answer.payload.unresolved_sentences_dict.get(sentence_id)
        answer = str(sentence.answer).replace(correct_date, answer_parts[1])
        self.send_confirm_answer(message_to_answer, answer, sentence.id)

    def handle_unresolved_sentences(self, handle_payload: help_center_data_type.MessageHandlePayload):
        unresolved_sentences = handle_payload.payload.unresolved_sentences
        for unresolved_sentence in unresolved_sentences:
            if unresolved_sentence.status.value == HandleSentenceStatus.NEED_MANAGER_ANSWER.value:
                matchers = re.findall(patterns, unresolved_sentence.answer)
                for manager_type in matchers:
                    if manager_type == correct_date:
                        self.handle_correct_date(handle_payload, unresolved_sentence)
                    if manager_type == deal_confirm:
                        self.deal_confirm(handle_payload, unresolved_sentence)
                    if manager_type == package_ind or manager_type == package_love or manager_type == package_family:
                        self.package_handle(handle_payload, unresolved_sentence, manager_type)

    def deal_confirm(self, handle_payload: help_center_data_type.MessageHandlePayload, unresolved_sentence):
        self.send_to_worker(handle_payload.user_name + ':')
        self.send_to_worker(unresolved_sentence.context)
        answer = str(unresolved_sentence.answer).replace(deal_confirm, '')
        self.send_confirm_answer(handle_payload, answer, unresolved_sentence.id)

    def package_handle(self, handle_payload: help_center_data_type.MessageHandlePayload, unresolved_sentence, manager_type: str):
        answer = str(unresolved_sentence.answer).replace(manager_type, package_answer[manager_type])
        self.send_confirm_answer(handle_payload, answer, unresolved_sentence.id)

    def handle_correct_date(self, handle_payload: help_center_data_type.MessageHandlePayload, unresolved_sentence):
        sentence_id = unresolved_sentence.id
        self.send_to_worker(sentence_id)
        self.send_to_worker(handle_payload.user_name + ':')
        self.send_to_worker(unresolved_sentence.context)
        self.send_to_worker('cor')
