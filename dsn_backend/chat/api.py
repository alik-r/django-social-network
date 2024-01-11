from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from .models import Chat, ChatMessage
from .serializers import ChatSerializer, ChatDetailSerializer, ChatMessageSerializer

@api_view(['GET'])
def chat_list(request):
    chats = Chat.objects.filter(users__in=list([request.user]))
    serializer  = ChatSerializer(chats, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def chat_detail(request, id):
    chat = Chat.objects.filter(users__in=list([request.user])).get(pk=id)
    serializer = ChatDetailSerializer(chat)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def chat_get_or_create(request, user_id):
    user = User.objects.get(pk=user_id)
    chats = Chat.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))
    chat = None

    if chats.exists():
        chat = chats.first()
    else:
        chat = Chat.objects.create()
        chat.users.add(user, request.user)
        chat.save()
    
    serializer = ChatDetailSerializer(chat)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def chat_send_message(request, id):
    chat = Chat.objects.filter(users__in=list([request.user])).get(pk=id)
    chat_message = ChatMessage.objects.create(
        chat=chat,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=chat.users.exclude(id=request.user.id).first(),
    )
    serializer = ChatMessageSerializer(chat_message)
    return JsonResponse(serializer.data, safe=False)
