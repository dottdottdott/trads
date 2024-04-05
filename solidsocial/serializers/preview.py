from rest_framework import serializers
from solidsocial.models import Preview

class PreviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    url = serializers.CharField(required=True)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    def create(self, validated_data):
        preview = Preview.objects.create(**validated_data)
        return preview
