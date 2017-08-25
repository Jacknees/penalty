from django import forms
from .models import Ambiente

class AmbienteForm(forms.ModelForm):
	nome = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Informe o nome do ambiente'}),)
	descricao = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Considerações sobre o ambiente'}),)
	endereco = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Informe o endereço do ambiente'}),)
	
	class Meta:
		model = Ambiente
		fields = ('nome', 'descricao', 'endereco')