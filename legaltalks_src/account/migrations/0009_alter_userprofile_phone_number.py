# Generated by Django 3.2.3 on 2021-05-22 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(default=None, max_length=10, null=True, unique=True),
        ),
    ]
