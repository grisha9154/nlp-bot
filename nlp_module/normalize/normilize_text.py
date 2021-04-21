import re

from nltk import word_tokenize
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords

patterns_ru = r'[^- а-яё]'
patterns_eng = r'[^ a-z]'
stopwords_ru = stopwords.words('russian')
stopwords_eng = stopwords.words('english')

language_type = 'rus'


morph = MorphAnalyzer()


def get_normalize_text(text):
    tokens = get_normalize_tokens(text)
    if tokens is None:
        return ''
    normalize_text = ' '.join(tokens)
    return normalize_text


def get_normalize_tokens(text: str) -> set[str] or None:
    lower_text = str(text).lower().strip()
    text_without_extra_char = get_text_without_extra_char(lower_text)
    word_tokens = word_tokenize(text_without_extra_char)
    tokens = set()

    stopwords_list = get_stop_words()

    for token in word_tokens:
        if token and token not in stopwords_list:
            token = token.strip()
            token = morph.normal_forms(token)[0]

            tokens.add(token)

    if len(tokens) > 0:
            return tokens
    return None


def get_text_without_extra_char(text):
    patterns = get_pattern()
    return re.sub(patterns, '', text)


def get_pattern():
    if language_type == 'eng':
        return patterns_eng
    else:
        return patterns_ru


def get_stop_words():
    if language_type == 'eng':
        return []
    else:
        return []
