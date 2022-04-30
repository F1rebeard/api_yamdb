"""
Скрипт заливки данных из csv в базу
Работает напрямую с моделями
Пример команды:
python manage.py load_scv *названия файлов, без расширения, через пробел*
Осторожно!!! Переписывает записи с существующими ID!!!
При необходимости менять ID записи в scv на свободный
"""


import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, GenreTitle, Review
from users.models import User
# Словарь допустимых параметров/названий файла
# Определяет модель, в которую будем заливать данные
# Дополнять по добавлению новых моделей
CHOICES = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': User,
    'review': Review
}
BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):
    # Считывает аргумены запуска через пробел
    # Аргументами являются названия файлов без расширения ака "users"
    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, **options):
        for file in options['csv_file']:
            model = CHOICES[file]
            csv_file = os.path.join(BASE_DIR, './static/data/' + file + '.csv')
            dataReader = csv.reader(
                open(csv_file, encoding='utf-8'),
                delimiter=',',
                quotechar='"'
            )
            next(dataReader)
            if model == User:  # Модель юзера нетипична, пришлось ручками
                print(file + ':')
                for row in dataReader:
                    print('    ', *row)
                    obj = model(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6]
                    )
                    obj.save()
            else:
                print(file + ':')
                for row in dataReader:
                    print('    ', *row)
                    obj = model(*row)
                    try:
                        obj.save()
                    except Exception as e:
                        print(e)
