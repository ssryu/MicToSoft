import csv
import numpy as np
from janome.tokenizer import Tokenizer




def csv_to_data(filename):
    texts, labels = [], []
    with open(filename) as file:
        file = csv.reader(file)
        for text, label in file:
            texts.append(text)
            labels.append(label)
    return texts, labels



def texts_to_vocab(tokenized_texts):
    vocab = []
    for tokenized_text in tokenized_texts:
        for word in tokenized_text:
            if word not in vocab:
                vocab.append(word)
    return vocab



def data_to_onehot(data):
    kind_data = []
    for datum in data:
        if datum not in kind_data:
            kind_data.append(datum)
    datum_to_id = dict(zip(kind_data, [i for i in range(len(kind_data))]))
    data_to_onehot = {}
    for datum in data:
        vec = np.zeros(len(kind_data))
        vec[datum_to_id[datum]] = 1
        data_to_onehot[datum] = vec
    return data_to_onehot, datum_to_id



class TextsTokenize:
    def __init__(self):
        self.t = Tokenizer()

    def __call__(self, texts):
        tokenized_texts = []
        for text in texts:
            tokenized_texts.append(self.text_tokenize(text))
        return tokenized_texts

    def text_tokenize(self, text):
        tokens = self.t.tokenize(text)
        tokenized_text = [token.base_form for token in tokens]
        return tokenized_text
