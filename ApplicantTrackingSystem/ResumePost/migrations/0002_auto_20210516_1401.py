# Generated by Django 3.0 on 2021-05-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ResumePost', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumepost',
            name='Applicant_name',
            field=models.CharField(max_length=255),
        ),
    ]
