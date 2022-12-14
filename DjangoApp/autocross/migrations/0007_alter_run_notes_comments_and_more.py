# Generated by Django 4.1.1 on 2022-12-03 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocross', '0006_best_run_data_cones_hit_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run_notes',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='run_notes',
            name='tire_pressure',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='run_notes',
            name='tire_wear',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='run_notes',
            name='video_link',
            field=models.URLField(blank=True, max_length=250),
        ),
    ]
