from .models import Book, SiteUser, Authenticator
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.http import QueryDict
from django.db.models.query import QuerySet
import json
import os
import hmac
from services import settings

# Create your views here.

def get_book(request):
    if request.method != "GET":
        return HttpResponse(json.dumps({"error":"incorrect method (use GET instead)"}), status=405)
    try:
        dict = QueryDict.request.GET.dict()
        qSet = Book.objects.filter(dict)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error":"Book not found"}), status=404)
    return HttpResponse(json.dumps(model_to_dict(qSet)), status=200)

def get_all_books(request):
    if request.method != "GET":
        return HttpResponse(json.dumps({"error":"incorrect method (use GET instead)"}), status=405)
    try:
        book_objects = Book.objects.all()
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    book_list = []
    for book in book_objects:
        book_list.append(model_to_dict(book))
    return HttpResponse(json.dumps(book_list), status=200)


def update_book(request, book_id):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)
    try:
        book_object = Book.objects.get(id=book_id)
        for key, value in request.POST.items():
            setattr(book_object, key, value)
        book_object.save()
        book_object = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error": "Book not found"}), status=404)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    return HttpResponse(json.dumps(model_to_dict(book_object)), status=200)


def create_book(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)

    try:
        title = request.POST["title"]
        ISBN = request.POST["ISBN"]
        author = request.POST["author"]
        price = request.POST["price"]
        year = request.POST["year"]
        class_id = request.POST["class_id"]
        edition = request.POST["edition"]
        type_name = request.POST["type_name"]
        condition = request.POST["condition"]
        seller_id = request.POST["seller"]
    except KeyError as e:
        return HttpResponse(json.dumps({"error": "Key not found: " + e.args[0]}), status=400)

    try:
        seller_object = SiteUser.objects.get(id=seller_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error": "Seller not found"}), status=500)

    try:
        book_object = Book(title=title, ISBN=ISBN, author=author, price=price, year=year, class_id=class_id,
                           edition=edition, type_name=type_name, condition=condition, seller=seller_object)
        book_object.save()
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    return HttpResponse(json.dumps(model_to_dict(book_object)), status=201)


def delete_book(request, book_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"error":"incorrect method (use GET instead)"}), status=405)
    try:
        book_object = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error":"Book not found"}), status=404)
    try:
        book_object.delete()
    except Exception as e:
        HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(json.dumps(model_to_dict(book_object)), status=200)

def get_user(request, user_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"error":"incorrect method (use GET instead)"}), status=405)
    try:
        user_object = SiteUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error":"User not found"}), status=404)
    user_json = json.dumps(model_to_dict(user_object))
    return HttpResponse(user_json, status=200)

def update_user(request, user_id):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)
    try:
        user_object = SiteUser.objects.get(id=user_id)
        for key, value in request.POST.items():
            if hasattr(user_object, key):
                setattr(user_object, key, value)

        user_object.save()
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error":"User not found"}), status=404)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    user_json = json.dumps(model_to_dict(user_object))
    return HttpResponse(user_json, status=200)


def create_user(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)

    try:
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        password = request.POST["password"]
        username = request.POST["username"]
        address = request.POST.get("address") or None
        user_object = SiteUser(name=name, phone=phone, email=email, password=password, username=username,
                               address=address, buyer_rating=0, seller_rating=0, buyer_activity_score=0,
                               seller_activity_score=0)
        user_object.save()
    except KeyError as e:
        return HttpResponse(json.dumps({"error": "Key not found: " + e.args[0]}), status=400)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    return HttpResponse(json.dumps(model_to_dict(user_object)), status=201)

def delete_user(request, user_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"error":"incorrect method (use GET instead)"}), status=405)
    try:
        user_object = SiteUser.objects.get(id=user_id)
        user_object.delete()
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error": "User not found"}), status=404)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(json.dumps(model_to_dict(user_object)), status=200)

def check_authenticator(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)

    try:
        authenticator = request.POST["authenticator"]
        auth_object = Authenticator.objects.get(authenticator=authenticator)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error": "Not logged in"}), status=401)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(json.dumps({"success": "User logged in", "user_id": auth_object.user.id}), status=200)

def login(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)

    try:
        username = request.POST["username"]
        password = request.POST["password"]
        user_list = SiteUser.objects.filter(username=username, password=password)
    except KeyError as e:
        return HttpResponse(json.dumps({"error": "Key not found: " + e.args[0]}), status=400)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    if len(user_list) == 0:
        return HttpResponse(json.dumps({"error": "Credentials invalid"}), status=401)
    elif len(user_list) > 1:
        return HttpResponse(json.dumps({"error": "More than one user has that login"}), status=401)
    else:
        user_object = user_list[0]

    authenticator = hmac.new(
        key=settings.SECRET_KEY.encode('utf-8'),
        msg=os.urandom(32),
        digestmod='sha256',
    ).hexdigest()
    try:
        authenticator_object = Authenticator(authenticator=authenticator, user=user_object)
        authenticator_object.save()
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    return HttpResponse(json.dumps({"authenticator": authenticator}), status=200)

def logout(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)
    try:
        authenticator = request.POST["authenticator"]
        auth_object = Authenticator.objects.get(authenticator=authenticator)
        auth_object.delete()
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error": "Not logged in"}), status=401)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(json.dumps({"success": "User logged out"}), status=200)
