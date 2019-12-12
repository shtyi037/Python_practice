from django.db import models

# Create your models here.
class Users(models.Model):
    uphone = models.CharField(max_length=20, verbose_name='聯絡方式')
    upass = models.CharField(max_length=50, verbose_name='密碼')
    uemail = models.EmailField(verbose_name='信箱')
    uname = models.CharField(max_length=20, null=True, verbose_name='用戶名')
    isActive = models.BooleanField(default=True, verbose_name='啟用')

    def __str__(self):
        return self.uname

    class Meta:
        db_table = 'users'
        verbose_name = '用戶'
        verbose_name_plural = verbose_name

class GoodsType(models.Model):
    title = models.CharField(max_length=30, verbose_name='類型名稱')
    desc = models.TextField(null=True, verbose_name='類型描述')
    picture = models.ImageField(
        upload_to='static/upload/goodstype', verbose_name='類型圖片')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'goodstype'
        verbose_name = '商品類型'
        verbose_name_plural = verbose_name

class Mos(models.Model):
    uphone = models.CharField(max_length=20, verbose_name='聯絡方式')
    upass = models.CharField(max_length=50, verbose_name='密碼')
    uemail = models.EmailField(verbose_name='信箱')
    uname = models.CharField(max_length=20, null=True, verbose_name='用戶名')
    isActive = models.BooleanField(default=True, verbose_name='啟用')