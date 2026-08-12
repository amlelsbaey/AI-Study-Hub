from django.contrib import admin
from .models import AIConversation, AIMessage
# Register your models here.

admin.site.register(AIConversation)
admin.site.register(AIMessage)