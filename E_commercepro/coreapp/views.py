from django.shortcuts import render, redirect
from coreapp.form import *
from django.contrib import messages

def index(request):
    products = Product.objects.all()
    return render(request, 'coreapp/index.html', {'products':products})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print("True")
            form.save()
            print("Data Saved Successfully")
            messages.success(request, "Product Added Successfully")
            return redirect("/")
        else:
            print("Not Working")
            messages.info("Product is not Added, Try Again")
    else:
        form = ProductForm()
    return render(request, "coreapp/add_product.html", {"form": form})
