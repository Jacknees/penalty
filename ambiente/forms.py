from django import forms
from .models import Ambiente, Evento
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date

class AmbienteForm(forms.ModelForm):
	nome = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Informe o nome do ambiente'}),)
	descricao = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Considerações sobre o ambiente'}),)
	endereco = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Informe o endereço do ambiente'}),)
	
	class Meta:
		model = Ambiente
		fields = ('nome', 'descricao', 'endereco')

class EventoForm(forms.ModelForm):
	nome = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Informe o nome do evento'}),)
	descricao = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Considerações sobre o evento'}),)
	valor_multa = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Valor da multa em R$'}),)
	quantidade_intervalos_repeticao = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Determine um intervalo'}),)
	data_inicio = forms.DateField(widget = forms.SelectDateWidget(), initial=date.today)
	data_fim = forms.DateField(widget = forms.SelectDateWidget(), initial=date.fromordinal(date.today().toordinal() + 30), error_messages = {'invalid': 'A data final deve ser maior que a inicial'})
	dia_evento = forms.DateField(widget = forms.SelectDateWidget(), initial=date.today)
	#responsavel = forms.CharField(widget=forms.Select(attrs={'class':'form-control'}),)

	class Meta:
		model = Evento
		fields = ('nome', 'descricao', 'responsavel', 'data_inicio', 'data_fim', 'dia_evento', 'valor_multa',
				'quantidade_intervalos_repeticao', 'intervalo')

	def __init__(self, participantes, *args, **kwargs):
		super(EventoForm, self).__init__(*args, **kwargs)
		self.fields['responsavel'].queryset = participantes

	def clean(self):
		cd = self.cleaned_data
		if cd.get('data_fim') < cd.get('data_inicio'):
			raise forms.ValidationError(self.fields['data_fim'].error_messages['invalid'])
			#self.add_error('Erro nas datas', "A data final deve ser maior que a inicial")
		return cd