# Generated by Django 4.1.3 on 2022-12-05 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssg_online_election_app', '0002_category_checkboxclass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='vote_by',
        ),
    ]
