from uuid import uuid4
from enum import Enum


class HandleSentenceStatus(Enum):
    OK = 0
    UNKNOWN = 1
    UPDATE = 2
    EMPTY_INPUT = 3
    NEED_MANAGER_ANSWER = 4


class HandleSentenceData:
    def __init__(self, context: str, sentence: str):
        self.id: str = str(uuid4())
        self.status: HandleSentenceStatus = HandleSentenceStatus.OK
        self.normalize_tokens: set[str] = None
        self.vector = None
        self.index: int = None
        self.answer: str = None
        self.context = context
        self.sentence = sentence


class HandleInputData:
    def __init__(self):
        self.unresolved_sentences: list[HandleSentenceData] = list()
        self.unresolved_sentences_dict: dict[str, HandleSentenceData] = dict()
        self.resolved_sentences: list[HandleSentenceData] = list()
        self.is_answer_ready: bool = True
