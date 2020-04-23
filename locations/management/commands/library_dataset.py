import os, csv

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from locations.models import Location, Type

class Command(BaseCommand):
    args = 'datasources/libraries.csv'
    help = 'Imports library data to database.'

    def handle(self, *args, **options):
        csvPath = self.args
        if not os.path.exists (csvPath):
            raise CommandError ("%s doesnt exist." %csvPath)

        # Csv Structure: LAT,LONG,Suburb/Town,Address,Phone
        csv_key = {
            'LAT' : 0,
            'LONG' : 1,
            'Suburb/Town': 2,
            'Address': 3,
            'Phone': 4
        }

        with open(csvPath) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            clean_dataset = []
            count = 0
            for row in reader:
                if (row[0] != '' and count > 3):
                    clean_dataset.append(row)
                count += 1

        library_type, created = Type.objects.get_or_create(name = 'library')
        library_type.save()

        for entry in clean_dataset:
            # print(int(entry[csv_key['LONG']]))
            point_location = Point(float(entry[csv_key['LONG']]), float(entry[csv_key['LAT']]))
            library, created = Location.objects.get_or_create(location = point_location)
            library.name = 'Library Services'
            library.address = entry[csv_key['Address']]
            library.suburb = entry[csv_key['Suburb/Town']]
            library.type = library_type
            library.save()
