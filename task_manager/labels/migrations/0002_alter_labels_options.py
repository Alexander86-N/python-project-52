# Generated by Django 4.1.2 on 2022-10-30 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("labels", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="labels",
            options={"verbose_name": "Label", "verbose_name_plural": "Labels"},
        ),
    ]