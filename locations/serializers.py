from rest_framework import serializers

from .models import Location, Type

class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ['id','name']


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location', 'name', 'type', 'website', 'suburb']
