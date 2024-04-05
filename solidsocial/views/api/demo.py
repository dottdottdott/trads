from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.reaction import ReactionSerializer
from solidsocial.serializers.message import MessageSerializer
from solidsocial.models import Post, Reaction, Message


class DemoAPI(APIView):
    def get(self, request, format=None):
        if 'clean' in request.GET: 
            if 'posts' in request.GET:
                posts = Post.objects.filter(id__gt=request.GET.get('posts'))
                for p in posts:
                    p.delete()
            if 'reactions' in request.GET:
                reactions = Reaction.objects.filter(id__gt=request.GET.get('reactions'))
                for r in reactions:
                    r.delete()
            return Response("Cleanup Done")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        if 'type' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.data['type'] == 'like':
            serializer = ReactionSerializer(data=request.data['data'])
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
        if request.data['type'] == 'message':
            serializer = MessageSerializer(data=request.data['data'])
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            

