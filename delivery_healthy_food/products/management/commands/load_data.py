import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from products.models import (
    Category, Product
)

#
# def read_users():
#     with open(
#             os.path.join(
#             settings.BASE_DIR,
#             'static', 'data', 'users.csv',
#             ),
#             'r', encoding='utf-8'
#     ) as f:
#         reader = csv.reader(f, delimiter=',')
#         for row in reader:
#             if row[0] == 'id':
#                 continue
#             User.objects.get_or_create(
#                 id=row[0],
#                 username=row[1],
#                 email=row[2],
#                 role=row[3],
#                 bio=row[4],
#                 first_name=row[5],
#                 last_name=row[6]
#             )
#     print('Данные из файла users.csv загружены')


def read_category():
    with open(
            os.path.join(
                settings.BASE_DIR,
                'data', 'category.csv',
            ),
            'r', encoding='utf-8'
    ) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == 'id':
                continue
            Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
    print('Данные из файла category.csv загружены')


# def read_genre():
#     with open(
#             os.path.join(
#                 settings.BASE_DIR,
#                 'static', 'data', 'genre.csv',
#             ),
#             'r', encoding='utf-8'
#     ) as f:
#         reader = csv.reader(f, delimiter=',')
#         for row in reader:
#             if row[0] == 'id':
#                 continue
#             Genre.objects.get_or_create(
#                 id=row[0],
#                 name=row[1],
#                 slug=row[2],
#             )
#     print('Данные из файла genre.csv загружены')
#
#
def read_products():
    with open(
            os.path.join(
                settings.BASE_DIR,
                'data', 'products.csv',
            ),
            'r', encoding='utf-8'
    ) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == 'id':
                continue
            Product.objects.get_or_create(
                id=row[0],
                name=row[1],
                measure_unit=row[2],
                amount=row[3],
                description=row[4],
                image=row[5],
                producer=row[6],
                category=row[7],
                price=row[8]
            )
    print('Данные из файла products.csv загружены')

#
# def read_genre_title():
#     with open(
#             os.path.join(
#                 settings.BASE_DIR,
#                 'static', 'data', 'genre_title.csv',
#             ),
#             'r', encoding='utf-8'
#     ) as f:
#         reader = csv.reader(f, delimiter=',')
#         for row in reader:
#             if row[0] == 'id':
#                 continue
#             GenreTitle.objects.get_or_create(
#                 id=row[0],
#                 title_id=row[1],
#                 genre_id=row[2],
#             )
#
#     print('Данные из файла genre_title.csv загружены')
#
#
# def read_review():
#     with open(
#             os.path.join(
#                 settings.BASE_DIR,
#                 'static', 'data', 'review.csv',
#             ),
#             'r', encoding='utf-8'
#     ) as f:
#         reader = csv.reader(f, delimiter=',')
#         for row in reader:
#             if row[0] == 'id':
#                 continue
#             Review.objects.get_or_create(
#                 id=row[0],
#                 title_id=row[1],
#                 text=row[2],
#                 author_id=row[3],
#                 score=row[4],
#                 pub_date=row[5]
#             )
#
#     print('Данные из файла review.csv загружены')
#
#
# def read_comments():
#     with open(
#             os.path.join(
#                 settings.BASE_DIR,
#                 'static', 'data', 'comments.csv',
#             ),
#             'r', encoding='utf-8'
#     ) as f:
#         reader = csv.reader(f, delimiter=',')
#         for row in reader:
#             if row[0] == 'id':
#                 continue
#             Comment.objects.get_or_create(
#                 id=row[0],
#                 review_id=row[1],
#                 text=row[2],
#                 author_id=row[3],
#                 pub_date=row[4]
#             )
#     print('Данные из файла comments.csv загружены')
#

class Command(BaseCommand):

    def handle(self, *args, **options):
        # read_users()
        read_category()
        read_products()
        # read_genre()


