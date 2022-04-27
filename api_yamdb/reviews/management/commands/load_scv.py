import csv

from django.core.management.base import BaseCommand

from reviews.models import Cathegory, Genre, Title

CHOICES = {
    'category': Cathegory,
    'genre': Genre,
    'titles': Title,
}


class Command(BaseCommand):
    help = 'import data'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)
        # this is optional so that your management command can just accept the
        # path of the csv instead of a hardcoded path
        # parser.add_argument(
        #     'csv_file',
        #     help='path to csv file',
        #     type=str)

    def handle(self, *args, **options):
        for file in options['csv_file']:
            model = CHOICES[file]
            csv_file = './static/data/' + file + '.csv'
            dataReader = csv.reader(
                open(csv_file),
                delimiter=',',
                quotechar='|'
            )
            for row in dataReader:
                if row[0] != 'id':
                    model.objects.create()
