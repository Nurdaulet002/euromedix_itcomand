# Generated by Django 3.0.5 on 2021-01-05 09:28

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rpn', '0001_initial'),
        ('sur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True)),
                ('size', models.CharField(max_length=10, null=True)),
                ('orientation', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=180, null=True)),
                ('kind', models.CharField(max_length=180, null=True)),
            ],
            options={
                'db_table': 'forms',
            },
        ),
        migrations.CreateModel(
            name='GroupForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180, null=True)),
            ],
            options={
                'db_table': 'groupForms',
            },
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=15, null=True)),
                ('position', models.IntegerField(null=True)),
                ('classes', models.CharField(max_length=80, null=True)),
                ('group', models.IntegerField(null=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='form.Form')),
            ],
            options={
                'db_table': 'rows',
            },
        ),
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('label', models.TextField(max_length=240, null=True)),
                ('kind', models.CharField(max_length=80, null=True)),
                ('colspan', models.CharField(max_length=80, null=True)),
                ('options', models.TextField(null=True)),
                ('is_bold', models.CharField(max_length=80, null=True)),
                ('is_italic', models.CharField(max_length=80, null=True)),
                ('is_center', models.CharField(max_length=80, null=True)),
                ('is_border', models.CharField(max_length=80, null=True)),
                ('is_rotated', models.CharField(max_length=80, null=True)),
                ('is_required', models.CharField(max_length=80, null=True)),
                ('visible', models.CharField(max_length=80, null=True)),
                ('grouping', models.CharField(max_length=80, null=True)),
                ('group_separator', models.CharField(max_length=80, null=True)),
                ('classes', models.CharField(max_length=80, null=True)),
                ('rowspan', models.IntegerField(null=True)),
                ('row', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='markers', to='form.Row')),
            ],
            options={
                'db_table': 'markers',
            },
        ),
        migrations.CreateModel(
            name='HospitalForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospFuncForms', to='form.Form')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groupForms', to='form.GroupForm')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospitalForms', to='sur.Hospital')),
            ],
            options={
                'db_table': 'hospitalForms',
            },
        ),
        migrations.CreateModel(
            name='FuncStructureForms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funcStructure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcStructureForms', to='sur.FuncStructure')),
                ('hospitalForms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funcStrucHospForms', to='form.HospitalForm')),
            ],
            options={
                'db_table': 'funcStructureForms',
            },
        ),
        migrations.CreateModel(
            name='DiseaseHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formData', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('status', models.IntegerField(null=True)),
                ('temporaryFormData', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('is_enabled', models.IntegerField(null=True)),
                ('in_archive', models.IntegerField(null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctoHistoryr', to=settings.AUTH_USER_MODEL)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formHistory', to='form.Form')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospitalHistory', to='sur.Hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patientHistory', to='rpn.Patient')),
                ('refererDoctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='refererDoctorHistory', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'diseaseHistory',
            },
        ),
        migrations.CreateModel(
            name='AdaptiveMarker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=180, null=True)),
                ('label', models.TextField(max_length=240, null=True)),
                ('options', models.TextField(null=True)),
                ('visible', models.CharField(max_length=80, null=True)),
                ('funcStructure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adapMarkerfuncStructure', to='sur.FuncStructure')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adapMarkerHospital', to='sur.Hospital')),
                ('marker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adapMarker', to='form.Marker')),
            ],
            options={
                'db_table': 'adaptiveMarker',
            },
        ),
    ]