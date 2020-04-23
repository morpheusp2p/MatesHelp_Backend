import os, csv, re

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from locations.models import Location, Type

class Command(BaseCommand):
    args = 'datasources/emergency-relief-provider-outlets-october-2016.csv'
    help = 'Imports emergency services data to database.'

    def handle(self, *args, **options):
        csvPath = self.args
        if not os.path.exists (csvPath):
            raise CommandError ("%s doesnt exist." %csvPath)

        # Csv Structure: Name(0),What(0),Who,Address 1,Address 2,Suburb,Phone,Phone 2,
        # Free Call,Email,Website,Twitter,Social Media,Monday,Tuesday,Wednesday,
        # Thursday,Friday,Saturday,Sunday,Public Holidays,Cost,Tram routes,
        # Bus routes,Nearest train station,Category 1,Category 2,Category 3,Category 4,Category 5,Category 6,
        #Longitude,Latitude,Geocoded Location
        # Organisation Legal Name(0),Outlet Name(1),Organistaion Website(2),Outlet Address(3),
        # Town or Suburb(4),Postcode(5),Activity External Name(6),SA2(7),SA3(8),SA4(9),LGA(10),Federal Electorate(11),
        # Latitude(12),Longitude(13),Location Withheld(14)
        csv_key = {
            'LAT' : 12,
            'LONG' : 13,
            'Suburb/Town': 4,
            'Address': 3,
            'Website': 2,
            'Name': 1,
            'Postcode': 5
        }

        with open(csvPath) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            clean_dataset = []
            count = 0
            for row in reader:
                if (row[0] != '' and count > 0):
                    clean_dataset.append(row)
                count += 1

        csv_type, created = Type.objects.get_or_create(name = 'Emegency Relief')
        csv_type.save()

        for entry in clean_dataset:
            if entry[csv_key['Postcode']].startswith("3"):
                # print(int(entry[csv_key['LONG']]))
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
