from django.contrib import admin

from .models import Page, Post

admin.site.register(Post)
admin.site.register(Page)
