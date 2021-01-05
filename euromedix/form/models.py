import json
from django.db import models
from django.conf import settings
from django.db.models import Count
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from sur.models import Hospital, FuncStructure
from rpn.models import Patient


# Список форм
class Form(models.Model):

    title = models.TextField(blank=True)
    # Форма бумаги A4 или А5 и тд
    size = models.CharField(max_length=10, null=True)
    # Альбомная ма или китап сиякты ма
    orientation = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=180, null=True)
    kind = models.CharField(max_length=180, null=True)

    def __str__(self):
        return self.title

    # Получить форму ИБ пациента
    def getHistoryForm(historyId):
        data = []
        groupedList = []
        patientHistory = DiseaseHistory.search({'historyId': historyId})
        formData = patientHistory.formData
        patientId = patientHistory.patient.id
        formId = patientHistory.form.id
        rows = Row.objects.filter(
            form__id=formId).select_related().order_by(
            'position').all()
        for row in rows:
            item = {
                'id': row.id,
                'markers': [],
            }
            for marker in row.markers.all():
                if marker.grouping != '0':
                    if marker.grouping not in groupedList:
                        markerFormData = ''
                        groupResult = Marker.objects.filter(
                            row__form__id=formId,
                            grouping=marker.grouping).all()
                        for markerGroup in groupResult:
                            markerGroupData = formData.get(
                                markerGroup.name, '')
                            if markerGroupData:
                                markerFormData += markerGroup.label
                                if markerGroup.kind == 'checkbox':
                                    for markerVal in markerGroupData:
                                        markerFormData += markerVal + ';'
                                else:
                                    separator = markerGroup.group_separator
                                    markerFormData += markerGroupData + separator
                        item['markers'].append(
                            {
                                'label': '',
                                'kind': 'groupedMarker',
                                'colspan': 12,
                                'formData': markerFormData
                            }
                        )
                        groupedList.append(marker.grouping)
                else:
                    markerFormData = formData.get(marker.name, '')
                    item['markers'].append(
                        {
                            'name': marker.name,
                            'label': marker.label,
                            'kind': marker.kind,
                            'colspan': marker.colspan,
                            'options': json.loads(marker.options),
                            'is_bold': marker.is_bold,
                            'is_italic': marker.is_italic,
                            'is_center': marker.is_center,
                            'visible': marker.visible,
                            'classes': marker.classes,
                            'formData': markerFormData
                        }
                    )
            if len(item['markers']) > 0:
                data.append(item)
        return data

    # Получить форму
    def getForm(searchData):
        data = []
        formData = {}
        tempFormData = {}
        parentFormData = {}
        historyId = searchData.get('historyId', '')
        doctor = searchData.get('doctor', '')
        if historyId:
            patientHistory = DiseaseHistory.search({'historyId': historyId})
            formData = patientHistory.formData
            tempFormData = patientHistory.temporaryFormData
            patientId = patientHistory.patient.id
            formId = patientHistory.form.id
        else:
            patientId = searchData.get('patientId', '')
            formId = searchData.get('formId', '')
        rows = Row.objects.filter(
            form__id=formId).select_related().order_by('position').all()
        adapMarkers = AdaptiveMarker.objects.select_related().filter(
            marker__row__id__in=rows, hospital__id=doctor.hospital.id,
            funcStructure__id=doctor.funcStructure.id, visible=1
        )
        for row in rows:
            item = {
                'id': row.id,
                'kind': row.kind,
                'markers': []
            }
            for marker in row.markers.all():
                parentData = ''
                try:
                    kind = marker.kind
                    adapMarker = adapMarkers.get(marker=marker.id)
                    label = adapMarker.label.replace('<br>', '\n')
                    adapMarkerKind = adapMarker.kind
                    options = adapMarker.options
                    if adapMarkerKind == 'parent':
                        parent = json.loads(options)
                        parentForm = parent['form_id']
                        parentMarkers = parent['markers']
                        for key, parentMarker in parentMarkers.items():
                            try:
                                if parentForm in parentFormData:
                                    pass
                                else:
                                    diseHistory = DiseaseHistory.objects
                                    parentHistory = diseHistory.filter(
                                        patient__id=patientId,
                                        form__id=parentForm
                                    ).last()
                                    if parentHistory:
                                        parentFormData[parentForm] = parentHistory.formData
                                Data = parentFormData.get(parentForm, '')
                                if Data:
                                    parentMarkerResult = Data.get(
                                        parentMarker, '')
                                    if parentMarkerResult:
                                        parentData += parentMarkerResult + ';'
                            except ObjectDoesNotExist:
                                pass
                except ObjectDoesNotExist:
                    label = marker.label.replace('<br>', '\n')
                    kind = marker.kind
                    options = marker.options
                item['markers'].append(
                    {
                        'id': marker.id,
                        'groupId': marker.grouping,
                        'name': marker.name,
                        'label': label,
                        'kind': kind,
                        'colspan': marker.colspan,
                        'options': json.loads(options),
                        'is_bold': marker.is_bold,
                        'is_italic': marker.is_italic,
                        'is_center': marker.is_center,
                        'visible': marker.visible,
                        'classes': marker.classes,
                        'formData': formData.get(marker.name, ''),
                        'tempFormData': tempFormData.get(marker.name, ''),
                        'parentData': parentData
                    }
                )
            data.append(item)
        return data

    class Meta:
        db_table = "forms"


# Столбцы формы
class Row(models.Model):
    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name='rows')
    kind = models.CharField(max_length=15, null=True)
    position = models.IntegerField(null=True)
    classes = models.CharField(max_length=80, null=True)
    group = models.IntegerField(null=True)

    class Meta:
        db_table = "rows"


# Маркеры формы
class Marker(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE,
                            related_name='markers')
    name = models.CharField(max_length=80)
    label = models.TextField(max_length=240, null=True)
    kind = models.CharField(max_length=80, null=True)
    colspan = models.CharField(max_length=80, null=True)
    options = models.TextField(null=True)
    is_bold = models.CharField(max_length=80, null=True)
    is_italic = models.CharField(max_length=80, null=True)
    is_center = models.CharField(max_length=80, null=True)
    is_border = models.CharField(max_length=80, null=True)
    is_rotated = models.CharField(max_length=80, null=True)
    is_required = models.CharField(max_length=80, null=True)
    visible = models.CharField(max_length=80, null=True)
    grouping = models.CharField(max_length=80, null=True)
    group_separator = models.CharField(max_length=80, null=True)
    classes = models.CharField(max_length=80, null=True)
    rowspan = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "markers"


# Группировка форм
class GroupForm(models.Model):
    title = models.CharField(max_length=180, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "groupForms"


# Формы больницы
class HospitalForm(models.Model):
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name='hospitalForms')
    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name='hospFuncForms')
    group = models.ForeignKey(GroupForm, on_delete=models.CASCADE,
                              null=True, related_name='groupForms')

    def search(searchData):
        data = []
        hospital = searchData.get('hospital', '')
        funcStructure = searchData.get('funcStructure', '')
        selectedByFuncStruc = searchData.get('selectedByFuncStruc', '')
        query = HospitalForm.objects
        if hospital:
            query = query.filter(hospital__id=hospital)
        if funcStructure:
            query = query.filter(
                funcStrucHospForms__funcStructure__id=funcStructure)
        groupList = query.values('group__id', 'group__title').annotate(
            dcount=Count('group__id'))
        for group in groupList:
            item = {
                'title': group['group__title'],
                'forms': [],
            }
            forms = query.filter(group__id=group['group__id'])
            for value in forms:
                isSelected = None
                if selectedByFuncStruc:
                    isSelected = value.funcStrucHospForms.filter(
                        funcStructure__id=selectedByFuncStruc).exists()
                item['forms'].append(
                    {
                        'id': value.form.id,
                        'title': value.form.title,
                        'isSelected': isSelected
                    }
                )
            data.append(item)
        return data

    class Meta:
        db_table = "hospitalForms"


# Формы отделении
class FuncStructureForms(models.Model):
    hospitalForms = models.ForeignKey(
        HospitalForm, on_delete=models.CASCADE,
        related_name='funcStrucHospForms')
    funcStructure = models.ForeignKey(
        FuncStructure, on_delete=models.CASCADE,
        related_name='funcStructureForms', null=True)

    class Meta:
        db_table = "funcStructureForms"


# ИБ пациента
class DiseaseHistory(models.Model):
    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name='formHistory')
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='patientHistory')
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='doctoHistoryr')
    formData = JSONField(null=True)
    refererDoctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='refererDoctorHistory', null=True)
    status = models.IntegerField(null=True)
    temporaryFormData = JSONField(null=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name='hospitalHistory')
    is_enabled = models.IntegerField(null=True)
    in_archive = models.IntegerField(null=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    # Искать ИБ пациента по критериям
    def search(searchData):
        patientId = searchData.get('patientId', '')
        historyId = searchData.get('historyId', '')
        query = DiseaseHistory.objects
        if historyId:
            return query.get(id=historyId)
        if patientId:
            query = query.filter(patient__id=patientId)
        return query.all()

    # Сохранить ИБ пациента
    def saveHistory(request, formId, historyId, status, patientId, doctor):
        formData = {}
        temporaryFormData = {}
        if historyId:
            formData = DiseaseHistory.objects.get(id=historyId).formData
        for rows in Row.objects.filter(form__id=formId).select_related():
            for marker in rows.markers.all():
                name = marker.name
                if marker.kind == 'checkbox':
                    value = request.getlist(name)
                else:
                    value = request.get(name, '')
                if value:
                    if status == '1' or status == '2':
                        formData.setdefault(name, value)
                    else:
                        temporaryFormData[name] = value

        obj, type_save = DiseaseHistory.objects.update_or_create(
            id=historyId,
            defaults={
                'formData': formData,
                'temporaryFormData': temporaryFormData,
                'doctor_id': doctor.id,
                'patient_id': patientId,
                'form_id': formId,
                'hospital_id': doctor.hospital.id,
                'status': status
            }
        )
        return obj.id

    class Meta:
        db_table = "diseaseHistory"


class AdaptiveMarker(models.Model):
    marker = models.ForeignKey(Marker, on_delete=models.CASCADE,
                               related_name='adapMarker')
    kind = models.CharField(max_length=180, null=True)
    label = models.TextField(max_length=240, null=True)
    options = models.TextField(null=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name='adapMarkerHospital')
    funcStructure = models.ForeignKey(
        FuncStructure, on_delete=models.CASCADE,
        related_name='adapMarkerfuncStructure')
    visible = models.CharField(max_length=80, null=True)

    class Meta:
        db_table = "adaptiveMarker"
