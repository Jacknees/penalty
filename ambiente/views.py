from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, get_list_or_404
from datetime import date
from .forms import AmbienteForm, EventoForm, EditEventoForm, Comentarios
from .models import Ambiente, User, Evento, ComentariosDeEventos
import PIL
from django.core.paginator import Paginator, InvalidPage, EmptyPage

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
	historico = Evento.objects.filter(id_agrupador=pkevento).filter(dia_evento__lt=date.today())
	paginator = Paginator(historico[::-1], 15) # Mostra 15 contatos por página

    # Make sure page request is an int. If not, deliver first page.
    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

	# Se o page request (9999) está fora da lista, mostre a última página.
	try:
		lista = paginator.page(page)
	except (EmptyPage, InvalidPage):
		lista = paginator.page(paginator.num_pages)

	return render(request, 'evento.html', {'ambiente':ambiente, 'evento':evento[0], 'historico':lista})

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

def tarefa(request, pk, pktarefa):
	ambiente = get_object_or_404(Ambiente, pk=pk)
	get_object_or_404(ambiente.participantes, pk=request.user.pk)
	eventobj = get_object_or_404(Evento, pk=pktarefa)
	comentarios = ComentariosDeEventos.objects.filter(evento=eventobj)
	form = Comentarios(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			com = form.save(commit=False)
			texto = form.cleaned_data['texto']
			com.usuario = request.user
			com.evento = eventobj
			com.save()
			return redirect('/ambiente/'+pk+'/tarefa/'+pktarefa+'/#post')
	return render(request, 'tarefa.html', {'ambiente':ambiente, 'tarefa':eventobj, 'coments':comentarios, 'form':form, 'regras':eventobj.action_rules(request.user), 'multa':eventobj.multa_corrente()})