# Generated by Django 3.2.3 on 2021-05-23 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_commonuserprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
