# Generated by Django 3.2.6 on 2021-08-14 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20210814_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='order',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
