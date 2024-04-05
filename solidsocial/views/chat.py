from django.shortcuts import render
from solidsocial.models import  Author, Message
from solidsocial.serializers.author import AuthorSerializer
from solidsocial.serializers.message import MessageSerializer


def ChatView(request, pk):
    messages = Message.objects.filter(correspondent=pk)
    author = Author.objects.get(id=pk)
    message_serializer = MessageSerializer(messages, many=True)
    author_serializer = AuthorSerializer(author)
    print(message_serializer.data)

    return render(request, "chat.html", {
        "current": "Chats", 
        "messages": message_serializer.data, 
        "author": author_serializer.data, 
        })
