# Generated by Django 2.1.7 on 2019-10-14 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technical_skill', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specializationskillexperience',
            name='specialization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='SpecializationSkillExperience', to='technical_skill.Specialization'),
        ),
    ]