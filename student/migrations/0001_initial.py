# Generated by Django 5.0.6 on 2025-03-27 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('job_type', models.CharField(choices=[('FT', 'Full-time'), ('PT', 'Part-time'), ('RM', 'Remote'), ('HY', 'Hybrid'), ('IO', 'In-office')], max_length=2)),
                ('job_mode', models.CharField(choices=[('FT', 'Full-time'), ('PT', 'Part-time'), ('RM', 'Remote'), ('HY', 'Hybrid'), ('IO', 'In-office')], max_length=2)),
                ('salary_range', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('internship_details', models.TextField(blank=True, null=True)),
                ('interview_mode', models.CharField(choices=[('ON', 'Online'), ('OF', 'Offline'), ('CP', 'CPN')], max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_postings', to='accounts.recruiter')),
            ],
        ),
    ]
