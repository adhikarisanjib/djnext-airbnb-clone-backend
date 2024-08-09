from django.contrib import admin

from chat.models import Conversation, ConversationMessage


admin.site.register(Conversation)
admin.site.register(ConversationMessage)
