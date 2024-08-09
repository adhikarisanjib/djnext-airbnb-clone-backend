from django.http import JsonResponse

from rest_framework.decorators import api_view

from useraccount.models import CustomUser
from chat.models import Conversation, ConversationMessage

from chat.serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer


@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users=request.user)
    serializer = ConversationListSerializer(conversations, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.get(id=pk)
    serializer = ConversationDetailSerializer(conversation)

    messages = ConversationMessage.objects.filter(conversation=conversation)
    messages_serializer = ConversationMessageSerializer(messages, many=True)

    return JsonResponse({"data": serializer.data, "messages": messages_serializer.data}, safe=False)


@api_view(['GET'])
def conversations_start(request, user_id):
    print("getting conversation list")
    conversations = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])
    if conversations.exists():
        conversations = conversations.first()
        return JsonResponse({"success": True, "conversation_id": conversations.id})
    
    conversation = Conversation.objects.create()
    user = CustomUser.objects.get(id=user_id)
    conversation.users.add(user)
    conversation.users.add(request.user)
    conversation.save()
    return JsonResponse({"success": True, "conversation_id": conversation.id})
