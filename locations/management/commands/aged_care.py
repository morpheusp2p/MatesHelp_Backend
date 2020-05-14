import os, csv, re

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from locations.models import Location, Type

class Command(BaseCommand):
    args = 'datasources/aged_care.csv'
    help = 'Imports centrelink locations to database.'

    def handle(self, *args, **options):
        csvPath = self.args
        if not os.path.exists (csvPath):
            raise CommandError ("%s doesnt exist." %csvPath)

        # Csv Structure: Service Name(0),Physical Address Line 1(1),Physical Address Line 2(2),Physical Address Suburb(3),
        # Physical Address State(4),Physical Address Post Code(5),2018 Aged Care Planning Region (ACPR)(6),Care Type(7),
        # Residential Places(8),Home Care Places(9),Restorative Care Places(10),Provider Name(11),Organisation Type(12),
        # ABS Remoteness(13),Latitude(14),Longitude(15),2018-19 Australian Government Funding(16)


        csv_key = {
            'LAT' : 14,
            'LONG' : 15,
            'Suburb/Town': 3,
            'Address1': 1,
            'Address2': 2,
            'Name': 0,
        }

        with open(csvPath) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            clean_dataset = []
            count = 0
            for row in reader:
                if (row[0] != '' and count > 0):
                    clean_dataset.append(row)
                count += 1

        csv_type, created = Type.objects.get_or_create(name = 'Aged Care Centre')
        csv_type.save()

        for entry in clean_dataset:
            # print(int(entry[csv_key['LONG']]))
            point_location = Point(float(entry[csv_key['LONG']]), float(entry[csv_key['LAT']]))
            location_service, created = Location.objects.get_or_create(location = point_location)
            location_service.name = entry[csv_key['Name']]
            location_service.address = entry[csv_key['Address1']]
            if entry[csv_key['Address2']]:
                location_service.address += ', '+entry[csv_key['Address1']]
            location_service.suburb = entry[csv_key['Suburb/Town']]
            location_service.type = csv_type
            location_service.save()
