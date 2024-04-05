from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from solidsocial.models import Author
from solidsocial.serializers.author import AuthorSerializer
from solidsocial.solidclient.social import init_solid_client, get_author


class AuthorsAPI(APIView):
    def get(self, request, format=None):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if "url" not in request.data:
            return Response("Url required", status=status.HTTP_400_BAD_REQUEST)
        else:
            sc = init_solid_client(True)
            return Response(get_author(sc, request.data['url'], False))
