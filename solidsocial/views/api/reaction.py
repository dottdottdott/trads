from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.reaction import ReactionSerializer
from solidsocial.models import Reaction

class ReactionAPI(APIView):
    def get(self, request, pk, format=None):
        reaction = Reaction.objects.get(pk=pk)
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)
