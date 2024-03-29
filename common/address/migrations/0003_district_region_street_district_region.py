# Generated by Django 4.2.3 on 2023-11-10 17:23

from django.db import migrations, models
import django.db.models.deletion

import csv
from collections import defaultdict

import os


csv_file_path_uz = os.path.join(os.getcwd(), 'common/address/migrations/soato_uz.csv')
csv_file_path_ru = os.path.join(os.getcwd(), 'common/address/migrations/soato_ru.csv')

def collect_data():
    regions = defaultdict(lambda: defaultdict(list))
    with open(csv_file_path_uz, 'r', encoding='utf-8') as csv_file_uz:
        csv_reader_uz = csv.reader(csv_file_uz)
        with open(csv_file_path_ru, 'r', encoding='utf-8') as csv_file:
            csv_reader_ru = csv.reader(csv_file)
            for row in csv_reader_ru:
                code, name = row[0], row[1].strip()
                if len(code) == 4:
                    level = 1
                elif len(code) == 7 and not code.endswith("00"):
                    level = 2
                elif len(code) > 7 and not code.endswith("00"):
                    level = 3
                else:
                    level = 4
                for row_uz in csv_reader_uz:
                    if row_uz[0] == code:
                        region_name_uz = row_uz[1].strip().title()
                        break

                if level == 1:
                    region_code = code
                    region_name = name.title()
                    regions[region_code]['name_uz'] = region_name_uz
                    regions[region_code]['name_ru'] = region_name
                    regions[region_code]['districts'] = []
                elif level == 2:
                    district_code = code
                    district_name = name.title()
                    regions[region_code]['districts'].append({'code': district_code,
                                                              'name_ru': district_name,
                                                              'name_uz': region_name_uz,
                                                              'streets': []}
                                                             )
                elif level == 3:
                    street_code = code
                    street_name = name.title()
                    regions[region_code]['districts'][-1]['streets'].append({'code': street_code,
                                                                             'name_ru': street_name,
                                                                             'name_uz': region_name_uz,
                                                                             })
    return regions


def create_objects(apps, schema_editor):
    data = collect_data()
    for region_code, region_data in data.items():
        Region = apps.get_model('address', 'Region')
        Region.objects.create(id=int(region_code), name_ru=region_data['name_ru'], name_uz=region_data['name_uz'])
        for district_data in region_data['districts']:
            District = apps.get_model('address', 'District')
            District.objects.create(id=int(district_data['code']),
                                    name_ru=district_data['name_ru'],
                                    name_uz=district_data['name_uz'],
                                    region_id=int(region_code))
            for street_data in district_data['streets']:
                Street = apps.get_model("address", "Street")
                Street.objects.create(id=int(street_data['code']),
                                      name_ru=street_data['name_ru'],
                                      name_uz=street_data['name_uz'],
                                      district_id=int(district_data['code']))


def reverse_create_objects(apps, schema_editor):
    ...



class Migration(migrations.Migration):
    dependencies = [
        ("address", "0002_alter_address_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="District",
            fields=[
                ("id", models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ("name_uz", models.CharField(max_length=100, verbose_name="Название UZ")),
                ("name_ru", models.CharField(max_length=100, verbose_name="Название RU")),
            ],
            options={
                "verbose_name": "Район ",
                "verbose_name_plural": "Районы ",
            },
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                ("id", models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ("name_uz", models.CharField(max_length=100, verbose_name="Название UZ")),
                ("name_ru", models.CharField(max_length=100, verbose_name="Название RU")),
            ],
            options={
                "verbose_name": "Область ",
                "verbose_name_plural": "Области ",
            },
        ),
        migrations.CreateModel(
            name="Street",
            fields=[
                ("id", models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ("name_uz", models.CharField(max_length=100, verbose_name="Название UZ")),
                ("name_ru", models.CharField(max_length=100, verbose_name="Название RU")),
                ("district", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="address.district")),
            ],
            options={
                "verbose_name": "Местность ",
                "verbose_name_plural": "Местности ",
            },
        ),
        migrations.AddField(
            model_name="district",
            name="region",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="address.region"),
        ),
        migrations.RunPython(create_objects, reverse_create_objects),
    ]
