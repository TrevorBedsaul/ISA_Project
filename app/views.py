from django.shortcuts import render
from .models import Book, Buyer, Seller, GenericUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound
import json

# Create your views here.

def test(request):
    return render(request, "test_template.html", {})

def get_book(request, book_id):
    if request.method != "GET":
        return HttpResponse(status=405)
    try:
        book_object = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({"Error":"Book not found"}))
    return HttpResponse(json.dumps(model_to_dict(book_object)), status=200)

@csrf_exempt
def update_book(request, book_id):
    if request.method != "POST":
        return HttpResponse(status=405)
    try:
        book_object = Book.objects.get(id=book_id)
        for key, value in request.POST.items():
            setattr(book_object, key, value)
        book_object.save()
        book_object = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({"Error":"Book not found"}))
    except:
        return HttpResponseNotFound(json.dumps({"Error":"Saving book failed"}))

    return HttpResponse(json.dumps(model_to_dict(book_object)), status=200)


@csrf_exempt
def create_book(request):
    if request.method != "POST":
        return HttpResponse(status=405)
    try:
        title = request.POST.get("title")
        ISBN = request.POST.get("ISBN")
        author = request.POST.get("author")
        price = request.POST.get("price")
        year = request.POST.get("year")
        class_id = request.POST.get("class_id")
        edition = request.POST.get("edition")
        type_name = request.POST.get("type")
        condition = request.POST.get("condition")
        seller_id = request.POST.get("seller")
    except:
        HttpResponse(status=400)

    try:
        seller_object = Seller.objects.get(id=seller_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({"Error":"Seller not found"}))

    try:
        book_object = Book(title=title, ISBN=ISBN, author=author, price=price, year=year, class_id=class_id,
                           edition=edition, type_name=type_name, condition=condition, seller=seller_object)
        book_object.save()
    except:
        HttpResponse(status=500)

    return HttpResponse(json.dumps(model_to_dict(book_object)), status=200)

def get_seller(request, seller_id):
    if request.method != "GET":
        return HttpResponse(status=405)
    try:
        seller_object = Seller.objects.get(id=seller_id)
        generic_user = seller_object.generic_user
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({"Error":"Seller not found"}))
    generic_user_dict = model_to_dict(generic_user)
    del generic_user_dict["password"]
    seller_dict = model_to_dict(seller_object)
    seller_dict["generic_user"] = generic_user_dict
    seller_json = json.dumps(seller_dict)
    return HttpResponse(seller_json, status=200)

@csrf_exempt
def update_seller(request, seller_id):
    if request.method != "POST":
        return HttpResponse(status=405)
    try:
        seller_object = Seller.objects.get(id=seller_id)
        generic_user = seller_object.generic_user

        for key, value in request.POST.items():
            if hasattr(seller_object, key):
                setattr(seller_object, key, value)
            else:
                setattr(generic_user, key, value)


        seller_object.generic_user =  generic_user
        seller_object.save()
        seller_object = Seller.objects.get(id=seller_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({"Error":"Seller not found"}))
    except:
        return HttpResponseNotFound(json.dumps({"Error":"Saving Seller failed"}))

    generic_user_dict = model_to_dict(generic_user)
    del generic_user_dict["password"]
    seller_dict = model_to_dict(seller_object)
    seller_dict["generic_user"] = generic_user_dict
    seller_json = json.dumps(seller_dict)

    return HttpResponse(seller_json, status=200)
