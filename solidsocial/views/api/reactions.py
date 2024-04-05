from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dssd.settings import SOLID_SETTINGS, DEMO
from solidsocial.serializers.reaction import ReactionSerializer
from solidsocial.solidclient.social import new_reaction
from solidsocial.models import Reaction

class ReactionsAPI(APIView):
    def get(self, request, format=None):
        if 'post' in request.GET: 
            reactions = Reaction.objects.filter(post=request.GET.get('post'))
        else:
            reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(new_reaction(request.data['post'], SOLID_SETTINGS['wid']))
