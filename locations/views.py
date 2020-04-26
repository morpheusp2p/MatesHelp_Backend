from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geos import Point, Polygon

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from .models import Location, Type
from .serializers import LocationSerializer, TypeSerializer

class WithinBoxFilterBackend(filters.BaseFilterBackend):

    param = 'ne'
    title = _('Within Box')
    description = _('Filter within a given box defined by two points (NE Longitude, NE Latitude, SW Lontigude, SW Latitude)')
    type = 'string'

    def filter_queryset(self, request, queryset, view):
        within_box_ne = request.query_params.get('ne', None)
        within_box_sw = request.query_params.get('sw', None)

        if within_box_ne is not None:
            within_box_ne = within_box_ne.split(',')
            if len(within_box_ne) == 2:
                ne_long = None
                ne_lat = None
            within_box_sw = within_box_sw.split(',')
            if len(within_box_sw) == 2:
                sw_long = None
                sw_lat = None

                try:
                    ne_long = float(within_box_ne[0])
                except:
                    print("Invalid NE Longitude") #TODO: Return query error
                    return queryset
                try:
                    ne_lat = float(within_box_ne[1])
                except:
                    print("Invalid NE Latitude") #TODO: Return query error
                    return queryset
                try:
                    sw_long = float(within_box_sw[0])
                except:
                    print("Invalid SW Longitude") #TODO: Return query error
                    return queryset
                try:
                    sw_lat = float(within_box_sw[1])
                except:
                    print("Invalid SW Latitude") #TODO: Return query error
                    return queryset

                if ne_long is not None and ne_long is not None and sw_long is not None and sw_lat is not None:
                    xmin = sw_long
                    ymin = sw_lat
                    xmax = ne_long
                    ymax = ne_lat
                    bbox = (xmin, ymin, xmax, ymax)
                    geom = Polygon.from_bbox(bbox)

                    #Filter by both places on screen, and disruptions on screen
                    queryset = queryset.filter(location__intersects=geom).distinct()

        return queryset

class TypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Types to be viewed or edited.
    """
    queryset = Type.objects.all().order_by('-id')
    serializer_class = TypeSerializer
    # permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """
    filter_backends = [
        WithinBoxFilterBackend
    ]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = [permissions.IsAuthenticated]
