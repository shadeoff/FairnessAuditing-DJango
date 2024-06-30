from django.db import models


# Create your models here.
class User(models.Model):
    GENDER_CHOICES = [
        (0, '男'),
        (1, '女'),
        (2, '未知'),
    ]

    CAREER_CHOICES = [
        (0, '审计工作者'),
        (1, '模型开发/研究人员'),
        (2, '普通用户(非技术人员)'),
    ]
    name = models.CharField(verbose_name="姓名", max_length=20)
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    company = models.CharField(verbose_name="单位", max_length=100)
    isKnowAI = models.BooleanField(verbose_name="是否接触过AI系统", default=False)
    isKnowFairness = models.BooleanField(verbose_name="是否接触过公平性概念", default=False)
    career = models.IntegerField(choices=CAREER_CHOICES, verbose_name="是否审计相关", default=0)
