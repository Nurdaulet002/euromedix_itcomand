from django.http import HttpResponse
from django.core import serializers
from .models import Patient


# Поиск пациента по содержанию
def search(request):
    searchData = {
        'searchText': request.POST.get('searchText', ''),
        'secondName': request.POST.get('secondName', ''),
        'firstName': request.POST.get('firstName', ''),
        'iin': request.POST.get('iin', ''),
        'patientId': request.POST.get('patientId', '')
    }
    list_patients = serializers.serialize(
        'json', Patients.search(searchData))
    return HttpResponse(list_patients)


