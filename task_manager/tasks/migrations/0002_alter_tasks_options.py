# Generated by Django 4.1.2 on 2022-10-30 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tasks",
            options={"verbose_name": "Task", "verbose_name_plural": "Tasks"},
        ),
    ]
