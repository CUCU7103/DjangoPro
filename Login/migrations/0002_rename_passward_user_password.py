# Generated by Django 4.2.2 on 2023-06-14 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Login", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="passward",
            new_name="password",
        ),
    ]
