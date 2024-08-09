from django.urls import path

from chat.api import conversation_list, conversation_detail, conversations_start


urlpatterns = [
    path('', conversation_list, name='conversation_list'),
    path('<uuid:pk>/', conversation_detail, name='conversation_detail'),
    path('start/<uuid:user_id>/', conversations_start, name='conversations_start'),
]
