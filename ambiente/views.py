from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, get_list_or_404
from .forms import AmbienteForm, EventoForm, EditEventoForm
from .models import Ambiente, User, Evento

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

def deletar_evento(request):
	if request.method == 'POST' and request.is_ajax():
		try:
			if request.POST.get('house') != "" and request.POST.get('idevent') != "":
				ambient = request.POST.get('house')
				event = request.POST.get('idevent')
				house = get_object_or_404(Ambiente, pk=ambient)
				get_object_or_404(house.participantes, pk=request.user.pk)
				if get_list_or_404(Evento, id_agrupador=event)[0].ambiente != house: raise Http404
				Evento.objects.filter(id_agrupador=event).delete()
				#house.participantes.remove(user)
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
			return redirect("/ambiente/{}/eventos/{}".format(pk, evento.id_agrupador))
	else:
		form = EventoForm(ambiente.participantes)
	return render(request, 'novo_evento.html', {'form':form, 'ambiente':ambiente})

def evento(request, pk, pkevento):
	ambiente = get_object_or_404(Ambiente, pk=pk)
	get_object_or_404(ambiente.participantes, pk=request.user.pk)
	evento = get_list_or_404(Evento, id_agrupador=pkevento)
	# participantes = ambiente.participantes.get_queryset()
	return render(request, 'evento.html', {'ambiente':ambiente, 'evento':evento[0]})

def editar_evento(request, pk, pkevento):
	ambiente = get_object_or_404(Ambiente, pk=pk)
	get_object_or_404(ambiente.participantes, pk=request.user.pk)
	inst_evento = get_list_or_404(Evento, id_agrupador=pkevento)[0]
	if inst_evento.ambiente != ambiente: raise Http404
	if request.method == 'POST':
		form = EditEventoForm(ambiente.participantes, request.POST, instance=inst_evento)
		if form.is_valid():
			evento = form.save(commit=False)
			# evento.criador = request.user
			# evento.ambiente = ambiente
			Evento.objects.filter(id_agrupador=inst_evento.id_agrupador).update(nome=evento.nome, descricao=evento.descricao, valor_multa=evento.valor_multa, responsavel=evento.responsavel)
			return redirect("/ambiente/{}/eventos/{}".format(pk, evento.id_agrupador))
	else:
		form = EditEventoForm(ambiente.participantes, instance=inst_evento)
	return render(request, 'editar_evento.html', {'form':form, 'ambiente':ambiente, 'evento':inst_evento})