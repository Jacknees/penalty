from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def index(request):	
	return render(request, 'index.html')

def login_page(request):
	if request.user.is_authenticated(): return index(request)
	return render(request, 'login.html')