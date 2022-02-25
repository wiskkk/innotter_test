from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from content_interaction.models import Like


class Name(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Tag(Name):
    pass


class Page(Name):
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('innotterapp.Tag', related_name='pages')
    owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('authentication.User', related_name='follows')
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('authentication.User', related_name='requests')
    unblock_date = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)
    likes = GenericRelation(Like)
    reply_to = models.ForeignKey('innotterapp.Post', on_delete=models.SET_NULL, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
