# coding: UTF-8
# サンプルコード
if __name__ == '__main__':
    import sys
    sys.path.append('プロジェクトディレクトリのフルパス')
    from learner import Learner, Classifier


    L = Learner()
    C = Classifier()
    
    # texts = ['振込がしたい', 'お金を引き出しにきた', '金よこせ', '預けようかな']
    # dataset = 'データセット'
    # wv_filename = '学習済wvモデル'


    # L.fit(dataset, wv_filename)
    # L.save('bank')


    # C.load('bank')
    # C.predict(texts)
