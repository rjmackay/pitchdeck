# Generated by Django 3.2.2 on 2021-05-14 03:28

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pitchdeck",
            name="processed",
            field=models.BooleanField(default=False),
        ),
    ]
