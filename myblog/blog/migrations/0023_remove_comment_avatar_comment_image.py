# Generated by Django 4.2.8 on 2024-03-07 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_comment_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='avatar',
        ),
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_pics/'),
        ),
    ]
