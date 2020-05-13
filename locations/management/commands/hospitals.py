import os, csv, re

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from locations.models import Location, Type

class Command(BaseCommand):
    args = 'datasources/Hospital_Locations.csv'
    help = 'Imports NPS data to database.'

    def handle(self, *args, **options):
        csvPath = self.args
        if not os.path.exists (csvPath):
            raise CommandError ("%s doesnt exist." %csvPath)

        # Csv Structure: X(0),Y(1),FID(2),LabelName(3),OpsName(4),Type(5),StreetNum(6),RoadName(7),
        # RoadType(8),RoadSuffix(9),CampusCode(10),LGAName(11),LocalityNa(12),
        # Postcode(13),VicgovRegi(14),State(15),ServiceNam(16)

        csv_key = {
            'LAT' : 1,
            'LONG' : 0,
            'Suburb/Town': 11,
            'StreetNum': 6,
            'RoadName': 7,
            'Name': 3,
            'Office-Type': 5,
        }

        with open(csvPath) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            clean_dataset = []
            count = 0
            for row in reader:
                if (row[0] != '' and count > 0):
                    clean_dataset.append(row)
                count += 1

        csv_type, created = Type.objects.get_or_create(name = 'Public Hospitals')
        csv_type.save()

        for entry in clean_dataset:
            if entry[csv_key['Office-Type']] == 'PUBLIC':
                point_location = Point(float(entry[csv_key['LONG']]), float(entry[csv_key['LAT']]))
                location_service, created = Location.objects.get_or_create(location = point_location)
                location_service.name = entry[csv_key['Name']]
                location_service.address = entry[csv_key['StreetNum']] +' ' + entry[csv_key['RoadName']]
                location_service.suburb = entry[csv_key['Suburb/Town']]
                location_service.type = csv_type

                location_service.save()
