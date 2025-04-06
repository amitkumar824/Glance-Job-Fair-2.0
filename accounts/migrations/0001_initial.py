# Generated by Django 5.0.6 on 2025-03-27 18:24

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('responsibilities', models.TextField()),
                ('skills', models.TextField()),
                ('departments', models.TextField()),
                ('company_interactions', models.TextField(blank=True, null=True)),
                ('registration_tracking', models.TextField(blank=True, null=True)),
                ('opening_deadlines', models.TextField(blank=True, null=True)),
                ('interview_coordination', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=200)),
                ('company_description', models.TextField()),
                ('company_website', models.URLField()),
                ('company_email', models.EmailField(max_length=254)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='company_logos/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=15, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('high_school', models.CharField(max_length=200)),
                ('current_year', models.IntegerField(help_text='Current academic year (1-4)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('graduation_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(2024), django.core.validators.MaxValueValidator(2030)])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('internship_details', models.TextField(blank=True, null=True)),
                ('cg_profile', models.TextField(blank=True, null=True)),
                ('is_final_year', models.BooleanField(default=False)),
                ('linkedin_profile', models.URLField(blank=True, null=True)),
                ('github_profile', models.URLField(blank=True, null=True)),
                ('google_certificate', models.FileField(blank=True, null=True, upload_to='certificates/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('active_backlog', models.IntegerField(default=0)),
                ('total_backlog', models.IntegerField(default=0)),
                ('password_year', models.IntegerField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx'])])),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('responsibilities', models.TextField()),
                ('skills', models.TextField()),
                ('departments', models.TextField()),
                ('event_management', models.TextField(blank=True, null=True)),
                ('support_roles', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
