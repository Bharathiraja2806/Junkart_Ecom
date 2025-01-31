from django.shortcuts import render, redirect
from coreapp.form import *
from django.contrib import messages
from django.utils import timezone

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

def product_desc(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "coreapp/product_des.html", {"product": product})


def add_to_cart(request, pk):

    # get that particular product id=pk
    product = Product.objects.get(pk = pk)

    # create order item
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )

     # Get Query set of Order Object of Particular User
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added Quantity Item")
            return redirect("product_desc", pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to Cart")
            return redirect("product_desc", pk=pk)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to Cart")
        return redirect("product_desc", pk=pk)



