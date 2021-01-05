from django.db import models
from sur.models import Hospital 

# Таблица пациентов
class Patient(models.Model):
    firstName = models.CharField(max_length=120)
    secondName = models.CharField(max_length=120)
    lastName = models.CharField(max_length=120, null=True, blank=True)
    birthDate = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    iin = models.CharField(max_length=15, null=True, blank=True)
    national = models.CharField(max_length=120, null=True, blank=True)
    citizen = models.CharField(max_length=120, null=True, blank=True)
    PersonID = models.CharField(max_length=120, null=True, blank=True)
    deathDate = models.DateField(blank=True, null=True)
    hGBD = models.CharField(max_length=120, null=True, blank=True)
    orgHealthCareId = models.CharField(max_length=120, null=True, blank=True)
    personAddressesID = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    placeWork = models.CharField(max_length=120, null=True, blank=True)
    profession = models.CharField(max_length=120, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    telephoneNumber = models.CharField(max_length=30, null=True, blank=True)
    personStatus = models.CharField(max_length=30, null=True, blank=True)
    typeRecorded = models.CharField(max_length=120, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.firstName


# получить список пациентов
def search(searchData):
    searchText = searchData.get('searchText', '')
    hospital = searchData.get('hospital', '')
    secondName = searchData.get('secondName', '')
    firstName = searchData.get('firstName', '')
    iin = searchData.get('iin', '')
    patientId = searchData.get('patientId', '')
    query = Patients.objects
    if patientId:
        return query.filter(id=patientId)[:1]
    if iin:
        query = query.filter(iin__icontains=iin)
    if hospital:
        query = query.filter(hospital=hospital)
    if firstName:
        query = query.filter(firstName__icontains=firstName)
    if secondName:
        query = query.filter(secondName__icontains=secondName)
    if searchText:
        query = query = query.annotate(fullName=Concat(
            'secondName', Value(' '), 'firstName')).filter(
            Q(iin__icontains=searchText) |
            Q(fullName__icontains=searchText))
    return query[:10]