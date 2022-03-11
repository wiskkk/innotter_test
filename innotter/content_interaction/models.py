from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from innotterapp.models import Page

from innotter import settings

# class Subscription(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscribers')
#     active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.user.email
#
#
# class Like(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes1')
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')


# class PageFollowing(models.Model):
#     page_id = models.ForeignKey('innotterapp.Page', related_name="followers", on_delete=models.CASCADE)
#     following_page_id = models.ForeignKey('innotterapp.Page', related_name="following", on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['page_id', 'following_page_id'], name="unique_followers")
#         ]
#
#         ordering = ["-created"]
#
#     def __str__(self):
#         return f"{self.page_id} follows {self.following_page_id}"
