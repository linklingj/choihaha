# Generated by Django 5.0.6 on 2024-08-15 08:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0011_question_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='down_voter',
            field=models.ManyToManyField(related_name='down_voter_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='voter',
            field=models.ManyToManyField(related_name='voter_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]

#aaaa