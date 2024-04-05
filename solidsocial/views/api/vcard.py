from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.vcard import VcardSerializer
from solidsocial.models import Vcard

class VcardAPI(APIView):
    def get(self, request, pk, format=None):
        vcards = Vcard.objects.get(pk=pk)
        serializer = VcardSerializer(vcards, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        vcard = Vcard.objects.get(pk=pk)
        vcard.delete()
        return Response("deleted", status=status.HTTP_200_OK)
