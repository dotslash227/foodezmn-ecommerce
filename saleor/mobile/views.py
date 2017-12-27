from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from saleor.product.models import Category, Product
from saleor.order.models import Order

@csrf_exempt
def signup(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request=request, email=email, password=password)
        if user:
            return HttpResponse("exists")
        else:
            message.success(request, _("User has been created"))
            return HttpResponse("done")

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request=request, email=username, password=password)
        if user is not None:
            return HttpResponse("true")
        else:
            return HttpResponse("false")

@csrf_exempt
def AllCategories(request):
    categories = Category.objects.all()
    data = serialize("json", categories)

    return JsonResponse(data, safe=False)

@csrf_exempt
def get_category(request):
    category_id = request.POST.get("cid")
    category = get_object_or_404(Category, id=category_id)
    if category:
        return HttpResponse(category)
    else:
        return HttpResponse("404")

@csrf_exempt
def recent_orders(request):
    email = request.POST.get("email")
    token = request.POST.get("token")
    orders = Order.objects.filter(user_email=email, token=token)

    data = serialize("json", orders)

    return JsonResponse(data, safe=False)

@csrf_exempt
def get_product_category_wise(request):
    category_id = request.POST.get("category_id")
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(categories__id=category.id)

    data = serialize("json", products)

    return JsonResponse(data, safe=False)

@csrf_exempt
def get_product(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)

    return HttpResponse(product)
