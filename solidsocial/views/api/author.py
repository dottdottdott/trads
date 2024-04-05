from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from solidsocial.models import Author
from solidsocial.serializers.author import AuthorSerializer


class AuthorAPI(APIView):
    def get(self, request, pk, format=None):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        author = Author.objects.get(pk=pk)
        author.delete()
        return Response("deleted", status=status.HTTP_200_OK)
