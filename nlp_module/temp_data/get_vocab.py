def get_vocab(sentence_list):
    vocab = set()
    for sentence in sentence_list:
        words = str(sentence).split()
        for word in words:
            vocab.add(word)

    return vocab
