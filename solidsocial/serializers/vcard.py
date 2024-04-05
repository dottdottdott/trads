from rest_framework import serializers
from solidsocial.models import Vcard, Author

class VcardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    #author_id = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(required=False, read_only=False, queryset=Author.objects.all())
    telephone = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    bday = serializers.DateField(required=False)
    role = serializers.CharField(required=False)
    note = serializers.CharField(required=False)
    address = serializers.JSONField(required=False)

    class Meta:
        model = Vcard
        depth = 1

    def create(self, validated_data):
        #if "author_id" in validated_data:
        #    validated_data['author'] = validated_data['author_id']
        #    validated_data.pop('author_id')
        vcard = Vcard.objects.create(**validated_data)
        return vcard
