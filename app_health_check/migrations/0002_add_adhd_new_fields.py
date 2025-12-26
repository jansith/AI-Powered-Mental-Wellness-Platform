# app_health_check/migrations/0002_add_adhd_new_fields.py
from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app_health_check', '0001_initial'),
    ]

    operations = [
        # First, add all new fields with null=True
        migrations.AddField(
            model_name='adhdquestionnaire',
            name='difficulty_sustaining_attention',
            field=models.IntegerField(
                null=True,
                blank=True,
                validators=[django.core.validators.MinValueValidator(0), 
                          django.core.validators.MaxValueValidator(3)]
            ),
        ),
        migrations.AddField(
            model_name='adhdquestionnaire',
            name='forgetful_daily_tasks',
            field=models.IntegerField(
                null=True,
                blank=True,
                validators=[django.core.validators.MinValueValidator(0), 
                          django.core.validators.MaxValueValidator(3)]
            ),
        ),
        migrations.AddField(
            model_name='adhdquestionnaire',
            name='poor_organization',
            field=models.IntegerField(
                null=True,
                blank=True,
                validators=[django.core.validators.MinValueValidator(0), 
                          django.core.validators.MaxValueValidator(3)]
            ),
        ),
        migrations.AddField(
            model_name='adhdquestionnaire',
            name='screen_time_daily',
            field=models.FloatField(
                null=True,
                blank=True,
                validators=[django.core.validators.MinValueValidator(1.0), 
                          django.core.validators.MaxValueValidator(10.0)]
            ),
        ),
        migrations.AddField(
            model_name='adhdquestionnaire',
            name='phone_unlocks_per_day',
            field=models.IntegerField(
                null=True,
                blank=True,
                validators=[django.core.validators.MinValueValidator(20), 
                          django.core.validators.MaxValueValidator(200)]
            ),
        ),
        migrations.AddField(
            model_name='adhdquestionnaire',
            name='working_memory_score',
            field=models.IntegerField(
                null=True,
                blank=True,
                validators=[django.core.validators.MinValueValidator(20), 
                          django.core.validators.MaxValueValidator(80)]
            ),
        ),
    ]