# Generated by Django 2.1.7 on 2019-10-16 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technical_skill', '0005_auto_20191015_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specializationskillexperience',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SpecializationSkillExperience', to='technical_skill.Specialization'),
        ),
    ]
