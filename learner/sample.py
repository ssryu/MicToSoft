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


    # L.fit(dataset)
    # L.fit(dataset, expected_acc_rate=0.8, n_re_learning=10)

    # L.save('bank')




    # C.load('bank')
    # C.predict(texts)
