from rest_framework import serializers

from solidsocial.models import Post

class NewPostSerializer(serializers.Serializer):
    content = serializers.CharField()
    reaction = serializers.CharField(required=False)
    signed = serializers.BooleanField(required=False)
