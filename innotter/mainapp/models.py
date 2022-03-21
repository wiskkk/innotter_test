from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Name(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Tag(Name):
    pass


class Page(Name):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    uuid = models.CharField(max_length=32, unique=True, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField('mainapp.Tag', related_name='pages', blank=True)
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    followers = models.ManyToManyField('mainapp.Page', blank=True, related_name='user_followers',
                                       symmetrical=False)
    following = models.ManyToManyField('mainapp.Page', blank=True, related_name='user_following',
                                       symmetrical=False)
    follow_requests = models.ManyToManyField('mainapp.Page', blank=True, related_name='followRequest',
                                             symmetrical=False)
    created_date = models.DateTimeField(auto_now_add=True)
    unblock_date = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, blank=True, related_name='likes', symmetrical=False)


class Reply(models.Model):
    owner = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE)
    reply_text = models.TextField(max_length=255)
    posts = models.ForeignKey(Post, verbose_name="post", on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return self.reply_text
