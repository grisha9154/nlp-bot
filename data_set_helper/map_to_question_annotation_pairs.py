from data_set_helper.data.question_answer_pair import QuestionAnswerPair


def map_to_question_answer_pair(info_list):
    pair_list = list()
    pair_element = QuestionAnswerPair()
    is_last_info_was_answer = True

    for info in info_list:
        if info.isQuestion:
            if is_last_info_was_answer:
                is_last_info_was_answer = False
                pair_list.append(pair_element)
                pair_element = QuestionAnswerPair(info.text)
            else:
                pair_element.question = pair_element.question + '.' + info.text
        else:
            if is_last_info_was_answer:
                pair_element.answer = pair_element.answer + '.' + info.text
            else:
                is_last_info_was_answer = True
                pair_element.answer = info.text

    pair_list.append(pair_element)

    return pair_list
