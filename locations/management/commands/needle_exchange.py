import os, csv, re

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from locations.models import Location, Type

class Command(BaseCommand):
    args = 'datasources/DHHS-NSP-Public - WebData.csv'
    help = 'Imports NPS data to database.'

    def handle(self, *args, **options):
        csvPath = self.args
        if not os.path.exists (csvPath):
            raise CommandError ("%s doesnt exist." %csvPath)

        # Csv Structure: NSPIS Agency(0),NSPIS(1),Model 1 Detail(2),Latitude(3),
        # Longitude(4),NSPIS Street Address(5),Place(6),Postcode(7),Opening hours(8)


        csv_key = {
            'LAT' : 3,
            'LONG' : 4,
            'Suburb/Town': 6,
            'Address': 5,
            'Name': 0,
            'Office-Type': 2,
            'OpeningHours': 8
        }

        with open(csvPath) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            clean_dataset = []
            count = 0
            for row in reader:
                if (row[0] != '' and count > 0):
                    clean_dataset.append(row)
                count += 1

        csv_type, created = Type.objects.get_or_create(name = 'Needle Exchange')
        csv_type.save()

        for entry in clean_dataset:
                point_location = Point(float(entry[csv_key['LONG']]), float(entry[csv_key['LAT']]))
                location_service, created = Location.objects.get_or_create(location = point_location)
                location_service.name = entry[csv_key['Name']] + '-' +entry[csv_key['Office-Type']]
                location_service.address = entry[csv_key['Address']]
                location_service.suburb = entry[csv_key['Suburb/Town']]
                location_service.type = csv_type
                timing_json = {
                    'Opening Hours': entry[csv_key['OpeningHours']]
                }
                location_service.opening_days = timing_json

                location_service.save()
