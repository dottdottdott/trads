from rest_framework import serializers
from solidsocial.models import Post, Author
from solidsocial.trust.trusteval import trusteval_post

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    author = serializers.PrimaryKeyRelatedField(required=False, read_only=False, queryset=Author.objects.all())
    content = serializers.CharField(required=False)
    checksum = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    signed = serializers.BooleanField(required=False)
    cdate = serializers.DateTimeField(required=False)
    pdate = serializers.DateTimeField(required=False)
    media = serializers.ImageField(required=False)
    response = serializers.PrimaryKeyRelatedField(required=False, read_only=False, queryset=Post.objects.all())
    trust_value = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'url', 'signed', 'cdate', 'media', 'response']
        depth = 2

    def create(self, validated_data):
        trust = trusteval_post(validated_data)
        validated_data['trust_value'] = trust
        post = Post.objects.create(**validated_data)
        return post
