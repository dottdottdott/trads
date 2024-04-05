from rest_framework import serializers
from solidsocial.models import Reaction, Post, Author
from solidsocial.trust.trusteval import trusteval_reaction

class ReactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    author = serializers.PrimaryKeyRelatedField(required=False, read_only=False, queryset=Author.objects.all())
    targetpost = serializers.PrimaryKeyRelatedField(required=False, read_only=False, queryset=Post.objects.all())
    content = serializers.CharField()
    signature = serializers.CharField(required=False)
    url = serializers.CharField(required=True)

    def create(self, validated_data):
        trusteval_reaction(validated_data)
        reaction = Reaction.objects.create(**validated_data)
        return reaction
