from django.db import models

class Motoboy(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Escala(models.Model):
    motoboy = models.ForeignKey(Motoboy, on_delete=models.CASCADE)
    data = models.DateField()
    turno = models.CharField(max_length=20)  # Manhã, Tarde, Noite

    def __str__(self):
        return f"{self.motoboy.nome} - {self.data} ({self.turno})"
