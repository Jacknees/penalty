from django.db import models
from django.utils import timezone
from datetime import date
from core.models import User

class Ambiente(models.Model):
	nome = models.CharField(max_length=100, verbose_name='Nome', null=False, blank=False)
	descricao = models.CharField(max_length=100, verbose_name='Descrição', null=True, blank=False)
	endereco = models.CharField(max_length=150, verbose_name='Endereço', null=True, blank=False)
	criador = models.ForeignKey(User, verbose_name='Criador', null=False, blank=False, related_name='+')
	data_criacao = models.DateTimeField(default=timezone.now)
	participantes = models.ManyToManyField(User, verbose_name='Participantes', blank=True, related_name='+')

	def __str__(self):
		return self.nome

class Evento(models.Model):
	INTERVALOS = (
        ('D', 'Dias'),
        ('S', 'Semanas'),
        ('M', 'Meses'),
    )
	nome = models.CharField(max_length=100, verbose_name='Nome', null=False, blank=False)
	descricao = models.CharField(max_length=100, verbose_name='Descrição', null=True, blank=False)
	criador = models.ForeignKey(User, verbose_name='Criador', null=False, blank=False, related_name='+')
	data_inicio = models.DateField(default=date.today)
	data_fim = models.DateField(verbose_name='Data de término')
	dia_evento = models.DateField()
	id_agrupador = models.IntegerField()
	valor_multa = models.FloatField(verbose_name='Valor da multa', blank=False, default=2.0)
	quantidade_intervalos_repeticao = models.IntegerField(verbose_name='Se repete em')
	intervalo = models.CharField(max_length=1, choices=INTERVALOS)
	solicitacao_de_validacao = models.BooleanField(default=False)
	momento_da_solicitacao = models.DateTimeField(blank=True)

	def __str__(self):
		return self.nome

# data do fim, data do evento, dia do evento, se repete em..., valor da multa, valido por..., 
# momento da validacao, solicitacao de validacao.