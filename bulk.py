import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailydive_project.settings')
django.setup()

from dailydive_webapp.models import solutions

f = open(r"./dailydive_solution.csv", 'r', encoding='utf-8-sig')
info = []

rdr = csv.reader(f)
for row in rdr:
    sentiment, solution_title, solution_guide, img_url = row
    tuple = (sentiment, solution_title, solution_guide, img_url)
    info.append(tuple)
f.close()

instances = []
for (sentiment, solution_title, solution_guide, img_url) in info:
    instances.append(solutions(sentiment=sentiment, solution_title=solution_title,
                              solution_guide=solution_guide,  img_url= img_url ))

solutions.objects.bulk_create(instances)
