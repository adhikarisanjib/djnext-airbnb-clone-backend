from rest_framework import serializers

from chat.models import Conversation, ConversationMessage

from useraccount.serializers import UserAccountDetailSerializer


class ConversationListSerializer(serializers.ModelSerializer):
    users = UserAccountDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'updated_at']


class ConversationDetailSerializer(serializers.ModelSerializer):
    users = UserAccountDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'updated_at']


    
class ConversationMessageSerializer(serializers.ModelSerializer):
    # conversation = ConversationListSerializer(read_only=True)
    sent_to = UserAccountDetailSerializer(read_only=True)
    created_by = UserAccountDetailSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = '__all__'


