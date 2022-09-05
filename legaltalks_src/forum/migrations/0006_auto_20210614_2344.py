# Generated by Django 3.2.3 on 2021-06-14 18:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0005_auto_20210614_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='downvotes',
            field=models.ManyToManyField(blank=True, related_name='a_downvoters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='a_upvoters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='downvotes',
            field=models.ManyToManyField(blank=True, related_name='q_downvoters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='q_upvoters', to=settings.AUTH_USER_MODEL),
        ),
    ]
