# Generated by Django 3.2.7 on 2021-09-23 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_lead_organisation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='Organisation',
        ),
    ]