# Generated by Django 4.0.6 on 2022-07-17 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='media', verbose_name='プロフィール画像'),
        ),
    ]
