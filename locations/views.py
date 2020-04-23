from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from .models import Location, Type
from .serializers import LocationSerializer, TypeSerializer

class TypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Types to be viewed or edited.
    """
    queryset = Type.objects.all().order_by('-id')
    serializer_class = TypeSerializer
    # permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = [permissions.IsAuthenticated]
