from django.shortcuts import render, redirect
from .forms import AmbienteForm

def novo_ambiente(request):
	if request.method == 'POST':
		form = AmbienteForm(request.POST)
		if form.is_valid():
			ambient = form.save(commit=False)
			ambient.criador = request.user
			ambient.participantes.add(request.user)
			ambient.save()
			return redirect("/")
	else:
		form = AmbienteForm()
	return render(request, 'novo_ambiente.html', {'form':form})
