from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.util.model import get_me
from solidsocial.util.helpers import get_base_url
from solidsocial.solidclient.social import init_solid_client, get_message

class MessagesUpdateAPI(APIView):
    def get(self, request, format=None):
        sc = init_solid_client(True)
        me = get_me()
        inbox = f"{get_base_url(me['url'])}/social/inbox"
        files = sc.get_foldercontent(inbox)
        messages = []
        for f in files:
            msg = get_message(sc, f['url'], True)
            if msg:
                messages.append(msg)
        return Response(messages, status=status.HTTP_200_OK)
