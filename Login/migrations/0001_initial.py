# Generated by Django 4.2.2 on 2023-06-14 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=255, verbose_name="id")),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("passward", models.CharField(max_length=255, verbose_name="Password")),
                ("email", models.EmailField(max_length=255)),
                ("registerd_dttm", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "userinfo",
            },
        ),
    ]
