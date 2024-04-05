from rest_framework import serializers
from solidsocial.models import Author
from solidsocial.trust.trusteval import trusteval_author

class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    name = serializers.CharField()
    url = serializers.CharField()
    trust_value = serializers.IntegerField(required=False)
    last_check = serializers.DateTimeField(required=False)
    followed = serializers.BooleanField(required=False)
    adddate = serializers.DateTimeField(required=False)
    photo = serializers.ImageField(required=False)
    key = serializers.CharField(required=False)

    def create(self, validated_data):
        trust = trusteval_author(validated_data)
        validated_data['trust_value'] = trust
        author = Author.objects.create(**validated_data)
        return author
