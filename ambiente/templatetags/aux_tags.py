from django import template
from ..models import Ambiente, User
# from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

register = template.Library()

@register.filter(name='typedata')
def typedata(value):
	if value == "D":
		return "dia(s)"
	elif value == "S":
		return "semana(s)"
	return "mes(es)"

@register.filter(name='firstnameaux')
def firstnameaux(value):
	return User.objects.get(pk=value).first_name