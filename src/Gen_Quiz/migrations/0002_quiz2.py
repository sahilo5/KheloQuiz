# Generated by Django 5.1.5 on 2025-01-24 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gen_Quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title1', models.TextField()),
                ('topic1', models.TextField()),
                ('noOfQuestions', models.TextField()),
            ],
        ),
    ]
