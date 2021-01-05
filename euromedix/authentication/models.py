from django.db import models
from django.contrib.auth.models import AbstractUser
from sur.models import Hospital, FuncStructure, Specialtie

# Таблица производных пользователей
class User(AbstractUser):
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, default="1")
    funcStructure = models.ForeignKey(
        FuncStructure, on_delete=models.CASCADE, default="1")
    specialty = models.ForeignKey(
        Specialtie, on_delete=models.CASCADE, default="1")

    @property
    # получить ФИО доктора
    def full_name(self):
        return self.last_name + ' ' + self.first_name