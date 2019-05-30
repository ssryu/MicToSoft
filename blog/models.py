from django.db import models
from django.utils import timezone

'''
モデルの定義

引数にmodelsを指定することでPostがジャンゴのモデルであり、
Postをデータベースに保存するようにする。
'''
class Post(models.Model):
    '''
    属性定義

    属性を定義するためにフィールド毎のデータの型を指定する。
    models.CharField : 文字数制限ありテキスト。
                タイトルのような短い文字列の保存に利用する。
    models.TextField : 文字数制限なしテキスト。
    models.DateTimeField : 日付と時間。
    models.ForeignKey : 他のモデルへのリンク。
    '''
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default = timezone.now)
    published_date = models.DateTimeField(
        blank = True, null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        '''
        タイトルをリターン
        '''
        return self.title