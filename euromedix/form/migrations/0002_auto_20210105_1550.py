# Generated by Django 3.1 on 2021-01-05 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseasehistory',
            name='formData',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='diseasehistory',
            name='temporaryFormData',
            field=models.JSONField(null=True),
        ),
    ]
