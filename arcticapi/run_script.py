#!/usr/bin/env python3

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcticapi.settings'
import django
django.setup()

# regular imports
from api.models import Category

# main script
def main():
    for cat in Category.objects.all():
        print(cat.id, cat.title)


# bootstrap
if __name__ == '__main__':
    main()