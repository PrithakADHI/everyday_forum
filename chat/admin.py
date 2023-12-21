from django.contrib import admin
from chat.models import Mychats
# Register your models here.

@admin.register(Mychats)
class MychatAdmin(admin.ModelAdmin):
    list_display = ('id','me','frnd','chats')