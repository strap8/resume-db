# Generated by Django 2.1.7 on 2019-10-16 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('technical_skill', '0004_specialization_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialization',
            name='author',
        ),
        migrations.AddField(
            model_name='specializationskillexperience',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='UserSpecialization', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='specializationskillexperience',
            name='specialization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='technical_skill.Specialization', verbose_name='SpecializationSkillExperience'),
        ),
    ]
