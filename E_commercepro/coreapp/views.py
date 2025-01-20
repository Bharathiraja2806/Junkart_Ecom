from django.shortcuts import render, redirect
from coreapp.form import *

def index(request):
    return render(request, 'coreapp/index.html')

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid:
           form.save()
        return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'coreapp/add_product.html', {'form': form})
