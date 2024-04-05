from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.preview import PreviewSerializer
from solidsocial.models import Preview
from solidsocial.solidclient.social import get_preview

class PreviewAPI(APIView):
    def get(self, request, format=None):
        if 'url' in request.GET: 
            return JsonResponse(get_preview(request.GET.get('url')))
        else:
            return Response("URL required", status=status.HTTP_400_BAD_REQUEST)
