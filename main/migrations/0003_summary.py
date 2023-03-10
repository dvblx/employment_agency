# Generated by Django 4.0.4 on 2023-01-11 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_applicant_user_alter_employer_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills', models.CharField(blank=True, max_length=60, verbose_name='Ключевые навыки')),
                ('information_about_yourself', models.TextField(verbose_name='О себе')),
                ('work_experience_information', models.TextField(blank=True, verbose_name='Об опыте работы')),
                ('additional_education', models.FileField(blank=True, null=True, upload_to='certificates')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.applicant', verbose_name='Соискатель')),
                ('education', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.education', verbose_name='Образование')),
            ],
        ),
    ]
