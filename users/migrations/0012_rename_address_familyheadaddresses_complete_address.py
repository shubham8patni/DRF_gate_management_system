# Generated by Django 4.2.2 on 2023-07-04 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_alter_familyheadaddresses_family_head_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="familyheadaddresses",
            old_name="address",
            new_name="complete_address",
        ),
    ]
