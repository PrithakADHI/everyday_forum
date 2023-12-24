from django.contrib import admin
from .models import Follower, Post, ExtraUser, Comment, Notification

# Register your models here.
admin.site.register(Follower)
admin.site.register(Post)
admin.site.register(ExtraUser)
admin.site.register(Comment)
admin.site.register(Notification)