from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from solidsocial.serializers.message import MessageSerializer
from solidsocial.models import Message
from dssd.settings import SOLID_SETTINGS
from solidsocial.solidclient.social import init_solid_client

class MessagesAPI(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sc = init_solid_client(True)
        meta = {} if "meta" not in request.data else request.data['meta']

        if "correspondant" in request.data:
            correspondant = request.data['correspondant']
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        msg = sc.new_message(correspondant, request.data['content'] if 'content' in request.data else None)
        data = {
                'url': msg['url'],
                'author': Author.objects.filter(url=SOLID_SETTINGS['wid'])[0].pk,
                }
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            print("valid")
            serializer.save()
        else:
            print(serializer.errors)
        return Response(serializer.data)
