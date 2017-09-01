from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import date
from core.models import User
from copy import copy
from django.db.models import Count

class Ambiente(models.Model):
	nome = models.CharField(max_length=100, verbose_name='Nome', null=False, blank=False)
	descricao = models.CharField(max_length=100, verbose_name='Descrição', null=True, blank=False)
	endereco = models.CharField(max_length=150, verbose_name='Endereço', null=True, blank=False)
	criador = models.ForeignKey(User, verbose_name='Criador', null=False, blank=False, related_name='+')
	data_criacao = models.DateTimeField(default=timezone.now)
	participantes = models.ManyToManyField(User, verbose_name='Participantes', blank=True, related_name='+')

	def __str__(self):
		return self.nome

	def listar_eventos_agregados(self):
		return Evento.objects.filter(ambiente=self.pk).values('nome', 'criador', 'responsavel', 'descricao', 'data_inicio', 'data_fim', 'quantidade_intervalos_repeticao', 'valor_multa', 'intervalo').annotate(dcount=Count('id_agrupador'))

class Evento(models.Model):
	INTERVALOS = (
        ('D', 'Dias'),
        ('S', 'Semanas'),
        ('M', 'Meses'),
    )
	nome = models.CharField(max_length=100, verbose_name='Nome', null=False, blank=False)
	descricao = models.CharField(max_length=100, verbose_name='Descrição', null=True, blank=False)
	criador = models.ForeignKey(User, verbose_name='Criador', null=False, blank=False, related_name='+', default=1)
	responsavel = models.ForeignKey(User, verbose_name='Responsavel pela tarefa', null=False, blank=False, related_name='+', default=1)
	ambiente = models.ForeignKey(Ambiente, verbose_name='Ambiente', null=False, blank=False, related_name='+')
	data_inicio = models.DateField(default=date.today)
	data_fim = models.DateField(verbose_name='Data de término')
	dia_evento = models.DateField()
	id_agrupador = models.IntegerField()
	valor_multa = models.FloatField(verbose_name='Valor da multa', blank=False, default=2.0)
	quantidade_intervalos_repeticao = models.IntegerField(verbose_name='Se repete em')
	intervalo = models.CharField(max_length=40, choices=INTERVALOS, null=False, blank=False)
	solicitacao_de_validacao = models.BooleanField(default=False)
	momento_da_solicitacao = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.nome

	def multipublish(self):
		try:
			self.id_agrupador = Evento.objects.last().id_agrupador + 1
		except AttributeError as e:
			self.id_agrupador = 1

		if self.intervalo == 'D':
			delta = self.data_fim - self.data_inicio
			for i in range(0, delta.days, self.quantidade_intervalos_repeticao):
				evento = copy(self)
				data = self.data_inicio.toordinal() + i
				evento.dia_evento = date.fromordinal(data)
				evento.save()

		elif self.intervalo == 'S':
			delta = self.data_fim - self.data_inicio
			for i in range(0, delta.days, 7 * self.quantidade_intervalos_repeticao):
				evento = copy(self)
				data = self.data_inicio.toordinal() + i
				evento.dia_evento = date.fromordinal(data)
				evento.save()

		elif self.intervalo == 'M':
			delta = self.data_fim - self.data_inicio
			meses = int(delta.days/30)
			for i in range(0, meses, self.quantidade_intervalos_repeticao):
				evento = copy(self)
				data = self.data_inicio + relativedelta(months=i)
				evento.dia_evento = data
				evento.save()





# data do fim, data do evento, dia do evento, se repete em..., valor da multa, valido por..., 
# momento da validacao, solicitacao de validacao.
# perto de meia noite