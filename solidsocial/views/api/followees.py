from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.models import Author
from solidsocial.serializers.author import AuthorSerializer

class FolloweesAPI(APIView):
    def get(self, request, format=None):
        followees = Author.objects.filter(followed=True)
        serializer = AuthorSerializer(followees, many=True)
        return Response(serializer.data)
