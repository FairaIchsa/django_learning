# Generated by Django 3.2.7 on 2021-09-23 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_rename_organisation_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organiser',
            field=models.BooleanField(default=False),
        ),
    ]