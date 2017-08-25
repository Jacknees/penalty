from django.shortcuts import render, HttpResponse, Http404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import User
import json

@login_required(login_url='/login')
def index(request):	
	return render(request, 'index.html')

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
