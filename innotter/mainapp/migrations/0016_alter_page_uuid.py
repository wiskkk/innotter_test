# Generated by Django 4.0.3 on 2022-03-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_alter_page_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='uuid',
            field=models.CharField(default='d526461be5fe4d75b272725d641e7993', max_length=32, unique=True),
        ),
    ]
