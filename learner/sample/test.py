from learner import Learner, Classifier



#L = Learner()
#L.fit('bank_dataset.csv', 'entity_vector.model.bin')
#L.save('bank')



text = ['振込をしにきました', '引き出してえ', 'あああああああ', '金を下ろしたい', '預けにきたんだけど', '振込しません']
C = Classifier()
C.load('bank')
C.predict(text)
