# Generated by Django 5.1.5 on 2025-03-30 06:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gen_Quiz', '0002_remove_quiz_noofquestions_remove_quiz_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2025, 3, 30)),
        ),
    ]
