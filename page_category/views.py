from django.shortcuts import render

from rest_framework import viewsets

from .serializers import PageSerializer
from .models import Page
# Create your views here.
class PageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Pages to be viewed or edited.
    """
    queryset = Page.objects.all().order_by('-id')
    serializer_class = PageSerializer
    # permission_classes = [permissions.IsAuthenticated]
