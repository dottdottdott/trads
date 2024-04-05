from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.preview import PreviewSerializer
from solidsocial.models import Preview

class PreviewsAPI(APIView):
    def get(self, request, format=None):
        previews = Preview.objects.all()
        serializer = PreviewSerializer(previews, many=True)
        return Response(serializer.data)
