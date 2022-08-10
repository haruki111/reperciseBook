from django.db import models
from django.contrib.auth import (
    get_user_model
)

# Create your models here.


class Tag(models.Model):
    name = models.CharField(verbose_name='タグ', max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(verbose_name='タイトル', max_length=100)
    description = models.TextField(
        verbose_name='説明', blank=True,
        null=True,
        max_length=1000,)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE, verbose_name='ユーザー')
    cover = models.ImageField(
        verbose_name='カバー', upload_to='media', blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    finish_count = models.IntegerField(verbose_name='周回', default=0)
    postData = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Book'


class Section(models.Model):
    title = models.CharField(verbose_name='タイトル', max_length=100)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='section')
    orderNum = models.IntegerField(verbose_name='順序', default=1000)

    def __str__(self):
        return self.title


class Problem(models.Model):
    question = models.TextField(verbose_name='設問', max_length=1000)
    answer = models.CharField(verbose_name='解答', max_length=255)
    explanation = models.TextField(
        verbose_name='解説', max_length=1000, blank=True, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='problem')
    orderNum = models.IntegerField(verbose_name='順序', default=1000)

    is_correct = models.BooleanField(verbose_name='正解したか', default=False)

    def __str__(self):
        return str(self.id) + "/" + str(self.section.title)
