from django.db import models
from django.utils import timezone
from core.models import User

class Ambiente(models.Model):
	nome = models.CharField(max_length=100, verbose_name='Nome', null=False, blank=False)
	descricao = models.CharField(max_length=100, verbose_name='Descrição', null=True, blank=False)
	endereco = models.CharField(max_length=150, verbose_name='Endereço', null=True, blank=False)
	criador = models.ForeignKey(User, verbose_name='Criador', null=False, blank=False, related_name='+')
	data_criacao = models.DateTimeField(default=timezone.now)
	participantes = models.ManyToManyField(User, verbose_name='Participantes', blank=True)

	def __str__(self):
		return self.nome
