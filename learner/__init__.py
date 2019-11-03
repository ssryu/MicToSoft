import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from gensim.models import KeyedVectors
import numpy as np
import pickle

from .preprocess import *




tokenizer = TextsTokenize()




# word_vectorの読み込み、重いので基本読み込まない
wmodel = None
def load_word_vector(word_vec):
    global wmodel
    if wmodel == None:
        wmodel = KeyedVectors.load_word2vec_format(word_vec, binary=True)




class Common:
    def __init__(self):
        self.id_to_label = None
        self.word_to_vec = None
        self.max_token = None
        self.vector_size = None
        self.model = None




class Learner(Common):
    def fit(self, filename, word_vec, max_token=20):
        load_word_vector(word_vec)

        # csvから文章とラベルを読み込み、形態素解析して単語リスト作る(ワードベクトルにない単語は除外)
        texts, labels = csv_to_data(filename)
        texts = tokenizer(texts)
        for i in range(len(texts)):
            texts[i] = [w for w in texts[i] if w in wmodel.vocab]
        vocab = texts_to_vocab(texts)

        # 形態素に分けられた文章達をRNNに入れるために整形、それぞれの単語をベクトルに変換する
        for text in texts:
            if max_token < len(text):
                max_token = len(text)
        g = np.zeros((len(texts), max_token, wmodel.vector_size))
        for i in range(len(texts)):
            for j in range(len(texts[i])):
                g[i][j][...] = wmodel.word_vec(texts[i][j])

        # ラベル達をRNNに入れるためにワンホットベクトルに変換して整形
        label_to_onehot, label_to_id = data_to_onehot(labels)
        h = np.zeros((len(labels), len(label_to_id)))
        for i in range(len(labels)):
            h[i][...] = label_to_onehot[labels[i]]

        # RNNのパラメータ達
        length_of_sequence = max_token
        in_neurons = g.shape[2]
        out_neurons = h.shape[1]
        n_hidden = 200

        # あとで必要そうなデータをオブジェクトに格納
        self.id_to_label = dict([(v, k) for k, v in label_to_id.items()])
        self.word_to_vec = {}
        for word in vocab:
            self.word_to_vec[word] = wmodel.word_vec(word)
        self.max_token = max_token
        self.vector_size = wmodel.vector_size

        # RNNの生成
        self.model = Sequential()
        self.model.add(LSTM(n_hidden, batch_input_shape=(None, length_of_sequence, in_neurons), return_sequences=False))
        self.model.add(Dense(out_neurons))
        self.model.add(Activation("sigmoid"))
        self.model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.001))
        early_stopping = EarlyStopping(monitor='val_loss', mode='auto', patience=20)
        self.model.fit(g, h, batch_size=300, epochs=100, validation_split=0.1, callbacks=[early_stopping], verbose=0)


    def save(self, filename):
        self.model.save(filename+'.keras', include_optimizer=False)
        self.model = None
        with open(filename+'.bin', 'wb') as f:
            pickle.dump(self, f)




class Classifier(Common):
    def load(self, filename):
        with open(filename+'.bin', 'rb') as f:
            damy = pickle.load(f)
        self.id_to_label = damy.id_to_label
        self.word_to_vec = damy.word_to_vec
        self.max_token = damy.max_token
        self.vector_size = damy.vector_size
        self.model = keras.models.load_model(filename+'.keras', compile=False)


    def predict(self, texts):
        tokenized_texts = tokenizer(texts)
        for i in range(len(tokenized_texts)):
            tokenized_texts[i] = [w for w in tokenized_texts[i] if w in self.word_to_vec]
        g = np.zeros((len(tokenized_texts), self.max_token, self.vector_size))
        for i in range(len(tokenized_texts)):
            for j in range(len(tokenized_texts[i])):
                g[i][j][...] = self.word_to_vec[tokenized_texts[i][j]]

        y = np.argmax(self.model.predict(g), axis=1)
        y = [self.id_to_label[y[i]] for i in range(len(y))]
        for text, label in zip(texts, y):
            print("%s : %s" % (text, label))
        return y
