from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.message import MessageSerializer
from solidsocial.models import Message

class MessageAPI(APIView):
    def get(self, request, pk, format=None):
        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)
