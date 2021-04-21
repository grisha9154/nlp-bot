class TempData:
    def __init__(self, df, vocab=None, temp_vectors=None):
        self.df = df
        self.vocab = vocab
        self.temp_vectors = temp_vectors

    def get_temp_list(self):
        return self.df['Context']
