# Generated by Django 5.0.6 on 2025-03-27 17:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('website', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=200)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('job_type', models.CharField(choices=[('FT', 'Full-time'), ('PT', 'Part-time'), ('IN', 'Internship'), ('CT', 'Contract'), ('TP', 'Temporary')], max_length=2)),
                ('job_mode', models.CharField(choices=[('RM', 'Remote'), ('HY', 'Hybrid'), ('IO', 'In-office'), ('FL', 'Flexible')], max_length=2)),
                ('salary_range', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('responsibilities', models.TextField()),
                ('required_skills', models.TextField()),
                ('interview_mode', models.CharField(choices=[('ON', 'Online'), ('OF', 'Offline'), ('CP', 'CPN')], max_length=2)),
                ('interview_date', models.DateTimeField()),
                ('number_of_openings', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('deadline', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='student.company')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_jobs', to='accounts.recruiter')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PD', 'Pending'), ('AC', 'Accepted'), ('RJ', 'Rejected'), ('WD', 'Withdrawn')], default='PD', max_length=2)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.job')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'ordering': ['-applied_at'],
            },
        ),
        migrations.AddField(
            model_name='job',
            name='applicants',
            field=models.ManyToManyField(blank=True, related_name='applied_jobs', through='student.JobApplication', to='accounts.student'),
        ),
        migrations.DeleteModel(
            name='JobPosting',
        ),
        migrations.AddIndex(
            model_name='jobapplication',
            index=models.Index(fields=['job', 'student'], name='student_job_job_id_81dddd_idx'),
        ),
        migrations.AddIndex(
            model_name='jobapplication',
            index=models.Index(fields=['status'], name='student_job_status_24c2a0_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='jobapplication',
            unique_together={('job', 'student')},
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['company', 'is_active'], name='student_job_company_69e38a_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['recruiter', 'is_active'], name='student_job_recruit_a9f8e9_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['deadline'], name='student_job_deadlin_475886_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['interview_date'], name='student_job_intervi_d6fae9_idx'),
        ),
    ]
