# Generated by Django 4.2.2 on 2023-07-01 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_myuser_options_alter_myuser_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="phone_number",
            field=models.CharField(db_index=True, max_length=10, unique=True),
        ),
    ]
