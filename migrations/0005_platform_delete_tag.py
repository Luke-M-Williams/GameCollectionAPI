# Generated by Django 4.2.10 on 2024-04-29 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameCollectionAPI', '0004_game_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
