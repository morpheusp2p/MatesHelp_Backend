import os, csv, re

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from locations.models import Location, Type

class Command(BaseCommand):
    args = 'datasources/Free_and_cheap_support_services__with_opening_hours__public_transport_and_parking_options__Helping_Out_.csv'
    help = 'Imports emergency services data to database.'

    def handle(self, *args, **options):
        csvPath = self.args
        if not os.path.exists (csvPath):
            raise CommandError ("%s doesnt exist." %csvPath)

        # Csv Structure: Name(0),What(1),Who(2),Address 1(3),Address 2(4),Suburb(5),Phone(6),Phone 2(7),
        # Free Call(8),Email(9),Website(10),Twitter(11),Social Media(12),Monday(13),Tuesday(14),Wednesday(15),
        # Thursday(16),Friday(17),Saturday(18),Sunday(19),Public Holidays(20),Cost(21),Tram routes(22),
        # Bus routes,(23)Nearest train station(24),Category 1(25),Category 2(26),Category 3(27),
        # Category 4(28),Category 5(29),Category 6(30), Longitude(31),Latitude(32),Geocoded Location(33)
        csv_key = {
            'LAT' : 31,
            'LONG' : 32,
            'Suburb/Town': 5,
            'Address': 3,
            'Website': 10,
            'Name': 0,
            'Category': 25
        }

        with open(csvPath) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            clean_dataset = []
            count = 0
            for row in reader:
                if (row[0] != '' and count > 0):
                    clean_dataset.append(row)
                count += 1

        # csv_type, created = Type.objects.get_or_create(name = 'Emegency Relief')
        # csv_type.save()

        for entry in clean_dataset:
            if (entry[csv_key['LONG']] and entry[csv_key['LAT']]) and (entry[csv_key['Category']] != 'N/A'):
                csv_type, created = Type.objects.get_or_create(name = entry[csv_key['Category']])
                csv_type.save()

                point_location = Point(float(entry[csv_key['LONG']]), float(entry[csv_key['LAT']]))
                location_service, created = Location.objects.get_or_create(location = point_location)
                location_service.name = entry[csv_key['Name']]
                location_service.address = entry[csv_key['Address']]
                extracted_url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', entry[csv_key['Website']])
                if len(extracted_url) == 0:
                    extracted_url = re.findall('http?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', entry[csv_key['Website']])
                if extracted_url:
                    location_service.website = extracted_url[0]
                location_service.suburb = entry[csv_key['Suburb/Town']]
                location_service.type = csv_type
                location_service.save()
