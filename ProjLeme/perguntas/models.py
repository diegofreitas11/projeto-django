from django.db import models
from django.db.models.options import Options

class Pesquisa(models.Model):
    id = models.AutoField(primary_key=True)
    pergunta = models.CharField(max_length=100, null=False)
    resposta1 = models.CharField(max_length=100, verbose_name="1ª alternativa")
    resposta2 = models.CharField(max_length=100, verbose_name="2ª alternativa")
    resposta3 = models.CharField(max_length=100, null=True, blank=True, verbose_name="3ª alternativa")
    resposta4 = models.CharField(max_length=100, null=True, blank=True, verbose_name="4ª alternativa")
    imagem = models.CharField(max_length=100, null=True, blank=True, verbose_name="Imagem (url)")


    class Meta:
        verbose_name = "Pesquisa Leme"
        verbose_name_plural = "Pesquisas"

    def __str__(self):
        return self.pergunta


class Envio(models.Model):
    id_envio = models.IntegerField()
    pergunta = models.CharField(max_length=100)
    resposta = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id_envio) + "º envio - " + str(self.pergunta)





# Create your models here.
