# Generated by Django 5.0 on 2023-12-24 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.post'),
        ),
        migrations.AddField(
            model_name='notification',
            name='url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
