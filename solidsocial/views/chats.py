from django.shortcuts import render
from solidsocial.models import Author, Message
from solidsocial.serializers.author import AuthorSerializer


def ChatsView(request):
    messages = Message.objects.all()
    authors = Author.objects.all()
    author_serializer = AuthorSerializer(authors, many=True)
    correspondents = list(Message.objects.values_list("correspondent",flat=True).order_by("correspondent").distinct())
    chats = []
    for c in correspondents:
        messages = Message.objects.filter(correspondent=c)
        newest = messages.order_by('-cdate').first()
        correspondent = Author.objects.get(pk=c)
        author_serializer = AuthorSerializer(correspondent)
        chats.append({
            'photo': author_serializer.data['photo'], 
            'name': author_serializer.data['name'], 
            'correspondent': author_serializer.data['id'], 
            'correspondenturl': author_serializer.data['url'], 
            'preview': newest.content, 
            })

    return render(request, "chats.html", {
        "current": "Chats", 
        "chats": chats, 
        })
