from uuid import uuid4

import input_hadler_module.data as input_handler_data_type


class MessageHandlePayload:
    def __init__(self, user_id: str, payload: input_handler_data_type.HandleInputData, user_name: str):
        self.id = str(uuid4())
        self.user_id = user_id
        self.payload = payload
        self.answer = ''
        self.user_name = user_name
