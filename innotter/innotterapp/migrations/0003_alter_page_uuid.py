# Generated by Django 4.0.2 on 2022-03-10 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innotterapp', '0002_alter_page_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='uuid',
            field=models.CharField(default='26c7dce8acb141cd8bf50eb910c411e6', max_length=32, unique=True),
        ),
    ]