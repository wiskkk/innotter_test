# Generated by Django 4.0.3 on 2022-03-15 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_remove_reply_parent_alter_page_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='uuid',
            field=models.CharField(default='9c9550fda53a469396bef28192cfe44f', max_length=32, unique=True),
        ),
    ]
