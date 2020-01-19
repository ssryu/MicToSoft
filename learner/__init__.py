import os

import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.optimizers import Adam, SGD
from keras.callbacks import EarlyStopping
from gensim.models import KeyedVectors, word2vec
import numpy as np
import pickle

from .preprocess import *




tokenizer = TextsTokenize()




# word_vector.model : 日本語wikiより作成
wv_filename = "word_vector.model"
wmodel = word2vec.Word2Vec.load(os.path.dirname(__file__) + '/' + wv_filename).wv




class Common:
    def __init__(self):
        self.id_to_label = None
        self.word_to_vec = None
        self.max_token = None
        self.vector_size = None
        self.model = None




class Learner(Common):
    # wv_filename は要らなくなったね　一応残す
    def fit(self, filename, wv_filename=None, max_token=40, expected_acc_rate=0.8, n_re_learning=3):
        '''
        モデルの作成と学習までをする
        通常はfilenameに渡されたデータセットからword2vectorのモデルも作成する
        他の学習ずみのwvモデルを使うときはそのファイル名をwv_filenameに渡すこと
        '''
        # csvから文章とラベルを読み込み、形態素解析して単語リスト作る(ワードベクトルにない単語は除外)
        texts, labels = csv_to_data(filename)
        batch_size = int(len(texts) / 20)
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
        n_hidden = 400

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
        self.model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.01), metrics=['acc'])
        early_stopping = EarlyStopping(monitor='val_loss', mode='auto', patience=15)
        his = self.model.fit(g, h, batch_size=batch_size, epochs=100, validation_split=0.1, callbacks=[early_stopping])#, verbose=0)

        #データの保持
        self.filename = filename
        self.acc = his.history['acc'][-1]

        #様子をみて再学習
        fit_n = 1
        while self.acc < expected_acc_rate and fit_n < n_re_learning:
            print('\n\nfit onemore!! {} / {}\n\n'.format(fit_n, n_re_learning))
            self.model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.01), metrics=['acc'])
            his = self.model.fit(g, h, batch_size=batch_size, epochs=100, validation_split=0.1, callbacks=[early_stopping])#, verbose=0)
            self.acc = his.history['acc'][-1]
            fit_n += 1

        if self.acc < expected_acc_rate:
            print('I failed to learn. acc-rate is {} under than {}'.format(self.acc, expected_acc_rate))



    def save(self, modelname):
        self.model.save(modelname+'.keras', include_optimizer=False)
        self.model = None
        with open(modelname+'.bin', 'wb') as f:
            pickle.dump(self, f)
        params = {
            'name' : modelname,
            'dataset' : self.filename,
            'acc' : self.acc,
        }
        return params




class Classifier(Common):
    def load(self, filename):
        with open(filename+'.bin', 'rb') as f:
            damy = pickle.load(f)
        self.id_to_label = damy.id_to_label
        self.word_to_vec = damy.word_to_vec
        self.max_token = damy.max_token
        self.vector_size = damy.vector_size
        self.model = keras.models.load_model(filename+'.keras', compile=False)
        #print(self.id_to_label)


    def predict(self, texts):
        if type(texts) is str: #単文の入力にも対応
            texts = [texts]
            a_text = True
        else:
            a_text = False

        tokenized_texts = tokenizer(texts)
        for i in range(len(tokenized_texts)):
            tokenized_texts[i] = [w for w in tokenized_texts[i] if w in self.word_to_vec]
        g = np.zeros((len(tokenized_texts), self.max_token, self.vector_size))
        for i in range(len(tokenized_texts)):
            for j in range(len(tokenized_texts[i])):
                g[i][j][...] = self.word_to_vec[tokenized_texts[i][j]]

        y = self.model.predict(g)
        y = np.argmax(y, axis=1)
        y = [self.id_to_label[y[i]] for i in range(len(y))]
        for text, label in zip(texts, y):
            print("%s : %s" % (text, label))

        if a_text:
            return y[0]
        return y
