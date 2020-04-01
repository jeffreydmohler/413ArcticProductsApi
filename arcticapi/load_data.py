#!/usr/bin/env python3

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcticapi.settings'
import django
django.setup()

# regular imports
from api.models import Category, Product
import json

# main script
def main():

    # read the json data
    with open('data.json') as json_data:
        data = json.load(json_data)

    cats = {}
    i = 1

    # find the categories, and replace them with the
    # new category id (created below)
    for prod in data['data'].values():
        if prod['category'] not in cats:
            cats[prod['category']] = i
            i += 1
        prod['category'] = cats[prod['category']]

    # create the categories
    for cat_name, cat_id in cats.items():
        new_cat = Category()
        new_cat.id = cat_id
        new_cat.title = cat_name
        new_cat.save()

    # create the products
    for prod in data['data'].values():
        p = Product()
        p.name = prod['name']
        p.description = prod['description']
        p.price = prod['price']
        p.filename = prod['filename']
        p.category = Category.objects.get(id=prod['category'])
        p.save()
    
    
if __name__ == '__main__':
    main()
