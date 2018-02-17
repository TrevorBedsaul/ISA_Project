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
        return HttpResponseNotFound('<h1>Book not found</h1>')
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
        return HttpResponseNotFound('<h1>Seller not found</h1>')

    try:
        book_object = Book(title=title, ISBN=ISBN, author=author, price=price, year=year, class_id=class_id,
                           edition=edition, type_name=type_name, condition=condition, seller=seller_object)
        book_object.save()
    except:
        HttpResponse(status=500)

    return HttpResponse(json.dumps(model_to_dict(book_object)), status=200)
