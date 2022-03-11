# Generated by Django 4.0.2 on 2022-03-10 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('innotterapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('following_page_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='innotterapp.page')),
                ('page_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='innotterapp.page')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddConstraint(
            model_name='pagefollowing',
            constraint=models.UniqueConstraint(fields=('page_id', 'following_page_id'), name='unique_followers'),
        ),
    ]
