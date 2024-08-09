import uuid

from django.db import models

from useraccount.models import CustomUser


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversation'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        
    def __str__(self):
        return f"{self.id}"
    

class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    sent_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversation_message'
        verbose_name = 'Conversation Message'
        verbose_name_plural = 'Conversation Messages'

    def __str__(self):
        return f"{self.body}"

