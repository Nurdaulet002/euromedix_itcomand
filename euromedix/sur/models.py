from django.db import models


# Список больниц
class Hospital(models.Model):
    title = models.CharField(max_length=120)
    address = models.CharField(max_length=180, null=True)

    class Meta:
        db_table = "hospital"


# Список отделении
class FuncStructure(models.Model):
    title = models.CharField(max_length=120)

    class Meta:
        db_table = "funcStructure"


# Список специальностей
class Specialtie(models.Model):
    title = models.CharField(max_length=120)

    class Meta:
        db_table = "specialtie"
