# Generated by Django 3.1 on 2020-10-19 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20201011_1129'),
        ('polls', '0004_question_value'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like',
            new_name='Likee',
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-created',)},
        ),
    ]
