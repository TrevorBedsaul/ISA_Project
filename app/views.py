from django.shortcuts import render
from .models import Book, Buyer, Seller, GenericUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def test(request):
    return render(request, "test_template.html", {})

def get_book(request, book_id):
    if request.method != "GET":
        return render(request, "error.txt", {})
    try:
        book_object = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return render(request, "error.txt", {})
    return render(request, "get_book_template.txt", {"book": book_object})

@csrf_exempt
def create_book(request):
    if request.method != "POST":
        return render(request, "error.txt", {})
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
        return render(request, "error.txt", {})

    try:
        seller_object = Seller.objects.get(id=seller_id)
    except ObjectDoesNotExist:
        return render(request, "error.txt", {})

    try:
        book_object = Book(title=title, ISBN=ISBN, author=author, price=price, year=year, class_id=class_id,
                           edition=edition, type_name=type_name, condition=condition, seller=seller_object)
        book_object.save()
    except:
        return render(request, "error.txt", {})
    return render(request, "create_book_template.txt", {"book_id": book_object.id})
