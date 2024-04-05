from rest_framework import serializers
from solidsocial.models import Message, Author
from solidsocial.trust.trusteval import trusteval_message

class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    url = serializers.CharField()
    correspondent = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Author.objects.all())
    received = serializers.BooleanField()
    content = serializers.CharField()
    signature = serializers.CharField(required=False)
    cdate = serializers.DateTimeField(required=False)
    seen = serializers.BooleanField(required=False)

    def create(self, validated_data):
        trusteval_message(validated_data)
        message = Message.objects.create(**validated_data)
        return message
