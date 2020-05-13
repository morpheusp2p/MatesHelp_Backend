from rest_framework import serializers

from .models import Page

class PageSerializer(serializers.HyperlinkedModelSerializer):
    # Type serializer
    class Meta:
        model = Page
        fields = ['id','name','banner_image','description','categories']
