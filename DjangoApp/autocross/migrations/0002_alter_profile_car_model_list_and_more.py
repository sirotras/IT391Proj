# Generated by Django 4.1.1 on 2022-09-28 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocross', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='car_model_list',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='car_num_list',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='run_list',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='suggestion_list',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='total_cone_count',
            field=models.IntegerField(blank=True),
        ),
    ]