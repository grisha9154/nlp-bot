import re

sentence_separator_regex = r'[.?!]'


def sentence_splitter(text: str) -> list[str]:
    sentences = re.split(sentence_separator_regex, text)
    return list(filter(filter_function, sentences))


def filter_function(sentence: str) -> bool:
    return sentence != ''
