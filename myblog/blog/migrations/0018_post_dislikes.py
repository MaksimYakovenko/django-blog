# Generated by Django 4.2.8 on 2024-01-08 16:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0017_remove_post_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(related_name='dislike_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
