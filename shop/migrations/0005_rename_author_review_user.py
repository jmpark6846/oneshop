# Generated by Django 3.2.6 on 2021-08-09 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_review_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='author',
            new_name='user',
        ),
    ]