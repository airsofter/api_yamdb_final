import csv
import os
import pandas as pd

from django.conf import settings
from django.core.management.base import BaseCommand
from progress.bar import IncrementalBar
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


df = pd.read_csv('static/data/category.csv', sep=',')
row_iter = df.iterrows()


def category_create():
    objs = [
        Category(
            name=row['name'],
            slug=row['slug']
        )
        for index, row in row_iter
    ]

    Category.objects.bulk_create(objs)


class Command(BaseCommand):
    """Команда для загрузки csv файлов в базу данных."""

    def handle(self, *args, **options):
        category_create()
        
