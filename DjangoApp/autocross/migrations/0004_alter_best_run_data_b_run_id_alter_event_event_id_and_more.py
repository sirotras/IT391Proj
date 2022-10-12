# Generated by Django 4.1.1 on 2022-10-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocross', '0003_alter_profile_total_cone_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='best_run_data',
            name='b_run_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='run_data',
            name='run_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='run_notes',
            name='note_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]