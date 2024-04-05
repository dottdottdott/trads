from rest_framework import serializers
# found at https://www.appsloveworld.com/django/100/118/passing-model-instances-by-id-in-serializer-django-rest-framework

class CustomForeignKeyField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return self.queryset

    def to_representation(self, value):
        value = super().to_representation(value)
        product = Product.objects.get(pk=value)
        return ProductSerializer(product).data

