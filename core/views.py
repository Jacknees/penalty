from django.shortcuts import render, HttpResponse, Http404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import User
from ambiente.models import Ambiente
import json

@login_required(login_url='/login')
def index(request):	
	meus_ambientes = Ambiente.objects.filter(participantes=request.user)
	return render(request, 'index.html', {'meus_ambientes': meus_ambientes})

def login_page(request):
	if request.user.is_authenticated(): return index(request)
	return render(request, 'login.html')

def entrar(request):
	if request.method == 'POST' and request.is_ajax():
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponse(json.dumps(True), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")
	raise Http404

def register(request):
	if request.method == 'POST' and request.is_ajax():
		userInstance = User()
		userInstance.first_name = request.POST.get('name')
		userInstance.username = request.POST.get('username')
		userInstance.email = request.POST.get('email')
		passw = request.POST.get('password')
		userInstance.set_password(passw)
		userInstance.save()
		print("user: "+ userInstance.username)
		print("senha: "+ passw)
		user = authenticate(username=userInstance.username, password=passw)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponse(json.dumps(True), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")
	raise Http404

def make_logout(request):	
	logout(request)
	return redirect("/")

def settings(request):
	if not request.user.is_authenticated():
		raise Http404
	else:
		#detalhes = get_object_or_404(Profile, user=request.user)
		#form = UserFormRegister(request.POST or None, instance=request.user)
		if request.POST:
			print('entrou na funçao')

			name = request.POST.get('first_name')
			#lastname = request.POST.get('last_name')
			#username = request.POST.get('username')
			email = request.POST.get('email')
			password = request.POST.get('password')
			repassword = request.POST.get('repassword')
			oldpassword = request.POST.get('oldpassword')
			print(name)
			#print(lastname)
			print(password)
			print(email)
			print(repassword)
			print(oldpassword)

			if name == '' or email == '' or password == '' or repassword == '' or oldpassword == '':
				return render(request, 'settings.html', {'error_name':'* Este campo é obrigatório.'})

			if request.user.check_password(oldpassword) == False:
				print('senha incorreta')
				return render(request, 'settings.html', {'error_de_senha': 'Senha atual está incorreta'})

			if password != repassword:
				return render(request, 'settings.html', {'error_de_reg': 'Senhas não conferem'})

			request.user.first_name = name
			request.user.email = email
			request.user.set_password(password)
			request.user.save()
			user = authenticate(username=request.user.username, password=password)
			login(request, user)
			#email_alteracao.delay(request.user.first_name, request.user.last_name, request.user.username, request.user.email)
			return render(request, 'settings.html', {'success':'Alteração feita com sucesso!'})
		return render(request, 'settings.html')

def excluiUser(request):
	if not request.user.is_authenticated():
		raise Http404
	else:
		if request.method == 'POST':
			idvi = request.POST.get('id')
			resultado = False
			if request.user.check_password(idvi) == True:
				request.user.delete()
				resultado = True
			return HttpResponse(json.dumps(resultado), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")