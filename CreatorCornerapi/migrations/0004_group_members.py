# Generated by Django 3.2.9 on 2021-12-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreatorCornerapi', '0003_auto_20211207_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='member', through='CreatorCornerapi.CreatorGroup', to='CreatorCornerapi.Creator'),
        ),
    ]
