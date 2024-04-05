from django.shortcuts import render
from solidsocial.models import Author
from solidsocial.serializers.author import AuthorSerializer

def UsersView(request):
    authors = Author.objects.all()
    author_serializer = AuthorSerializer(authors, many=True)
    
    return render(request, "users.html", {"current": "Users", "authors": author_serializer.data})
