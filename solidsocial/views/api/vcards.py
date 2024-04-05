from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.vcard import VcardSerializer
from solidsocial.models import Vcard

class VcardsAPI(APIView):
    def get(self, request, format=None):
        vcards = Vcard.objects.all()
        serializer = VcardSerializer(vcards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VcardSerializer(data=request.POST['data'])
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return Response(serializer.data)
