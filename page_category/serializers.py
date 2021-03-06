from rest_framework import serializers

from .models import Page

class PageSerializer(serializers.ModelSerializer):
    # Type serializer
    class Meta:
        model = Page
        fields = ['id','name','slug','banner_image','description','categories']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
