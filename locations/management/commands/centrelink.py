import os, csv, re

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from locations.models import Location, Type

class Command(BaseCommand):
    args = 'datasources/centrelink-office-locations-as-at-24-march-2020.csv'
    help = 'Imports centrelink locations to database.'

    def handle(self, *args, **options):
        csvPath = self.args
        if not os.path.exists (csvPath):
            raise CommandError ("%s doesnt exist." %csvPath)

        # Csv Structure: OFFICE TYPE(0),SITE NAME(1),ALTERNATIVE NAME(2),ADDRESS(3),SUBURB(4),STATE(5),POSTCODE(6),
        # LATITUDE(7),LONGITUDE(8),OPEN(9),CLOSE(10),CLOSED FOR LUNCH(0)

        csv_key = {
            'LAT' : 7,
            'LONG' : 8,
            'Suburb/Town': 4,
            'Address': 3,
            'Name': 1,
            'Office-Type': 0,
            'State': 5
        }

        with open(csvPath) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            clean_dataset = []
            count = 0
            for row in reader:
                if (row[0] != '' and count > 0):
                    clean_dataset.append(row)
                count += 1

        csv_type, created = Type.objects.get_or_create(name = 'Centrelink')
        csv_type.save()

        for entry in clean_dataset:
            if entry[csv_key['State']] == 'VIC':
                # print(int(entry[csv_key['LONG']]))
                point_location = Point(float(entry[csv_key['LONG']]), float(entry[csv_key['LAT']]))
                location_service, created = Location.objects.get_or_create(location = point_location)
                location_service.name = entry[csv_key['Name']] + '-' +entry[csv_key['Office-Type']]
                location_service.address = entry[csv_key['Address']]
                location_service.suburb = entry[csv_key['Suburb/Town']]
                location_service.type = csv_type
                location_service.save()
