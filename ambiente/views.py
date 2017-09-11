from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import AmbienteForm, EventoForm
from .models import Ambiente, User

import json

def novo_ambiente(request):
	if request.method == 'POST':
		form = AmbienteForm(request.POST)
		if form.is_valid():
			ambient = form.save(commit=False)
			ambient.criador = request.user
			ambient.save()
			ambient.participantes.add(request.user)
			return redirect("/")
	else:
		form = AmbienteForm()
	return render(request, 'novo_ambiente.html', {'form':form})

def detalhe_ambiente(request, pk):
	ambiente = get_object_or_404(Ambiente, pk=pk)
	get_object_or_404(ambiente.participantes, pk=request.user.pk)
	participantes = ambiente.participantes.values()
	return render(request, 'detalhe_ambiente.html', {'ambiente':ambiente, 'participantes':participantes})

def participantes(request, pk):
	ambiente = get_object_or_404(Ambiente, pk=pk)
	get_object_or_404(ambiente.participantes, pk=request.user.pk)
	participantes = ambiente.participantes.get_queryset()
	return render(request, 'participantes.html', {'ambiente':ambiente, 'participantes':participantes})

def remove_user(request):
	if request.method == 'POST' and request.is_ajax():
		try:
			if request.POST.get('iduser') != "" and request.POST.get('house') != "":
				ambient = request.POST.get('house')
				user = request.POST.get('iduser')
				house = get_object_or_404(Ambiente, pk=ambient)
				if house.criador != request.user: raise Http404
				house.participantes.remove(user)
				return HttpResponse(json.dumps(True), content_type="application/json")
			return HttpResponse(json.dumps(False), content_type="application/json")
		except Exception as e:
			print(e)
			return HttpResponse(json.dumps(False), content_type="application/json")
	raise Http404

def add_user(request):
	if request.method == 'POST' and request.is_ajax():
		try:
			if request.POST.get('email') != "" and request.POST.get('house') != "":
				ambient = request.POST.get('house')
				email = request.POST.get('email')
				house = get_object_or_404(Ambiente, pk=ambient)
				if house.criador != request.user: raise Http404
				house.participantes.add(User.objects.get(email=email))
				return HttpResponse(json.dumps(True), content_type="application/json")
			return HttpResponse(json.dumps(False), content_type="application/json")
		except Exception as e:
			print(e)
			return HttpResponse(json.dumps(False), content_type="application/json")
	raise Http404

def eventos(request, pk):
	ambiente = get_object_or_404(Ambiente, pk=pk)
	get_object_or_404(ambiente.participantes, pk=request.user.pk)
	# participantes = ambiente.participantes.get_queryset()
	return render(request, 'eventos_ambiente.html', {'ambiente':ambiente, 'eventos':ambiente.listar_eventos_agregados()})

def new_evento(request, pk):
	ambiente = get_object_or_404(Ambiente, pk=pk)
	get_object_or_404(ambiente.participantes, pk=request.user.pk)
	if request.method == 'POST':
		form = EventoForm(ambiente.participantes, request.POST)
		if form.is_valid():
			evento = form.save(commit=False)
			evento.criador = request.user
			evento.ambiente = ambiente
			evento.multipublish()
			return redirect("/ambiente/{}/eventos".format(pk))
	else:
		form = EventoForm(ambiente.participantes)
	return render(request, 'novo_evento.html', {'form':form, 'ambiente':ambiente})
