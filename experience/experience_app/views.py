from django.http import HttpResponse
import json
import urllib.request
from urllib.error import HTTPError


# Create your views here.

def home(request):
    req = urllib.request.Request('http://models-api:8000/api/v1/books/all')
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(resp_json, status=200)


def book_detail(request, book_id):
    book_req = urllib.request.Request('http://models-api:8000/api/v1/books/' + str(book_id))

    try:
        book_json = urllib.request.urlopen(book_req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    book = json.loads(book_json)
    seller_id = book['seller']
    has_buyer = (book['buyer'] != None)
    seller_req = urllib.request.Request('http://models-api:8000/api/v1/users/' + str(seller_id))
    try:
        seller_json = urllib.request.urlopen(seller_req).read().decode('utf-8')
        if has_buyer:
            buyer_req = urllib.request.Request('http://models-api:8000/api/v1/users/' + str(book['buyer']))
            buyer_json = urllib.request.urlopen(buyer_req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    seller = json.loads(seller_json)
    book['seller'] = {'id':seller['id'], 'name':seller['name']}
    if has_buyer:
        buyer = json.loads(buyer_json)
        book['buyer'] = {'id': buyer['id'], 'name': buyer['name']}
    return HttpResponse(json.dumps(book), status=200)

def login(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)

    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except KeyError as e:
        return HttpResponse(json.dumps({"error": "Key not found: " + e.args[0]}), status=400)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    post_data = {'username': username, 'password': password}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/login', data=post_encoded, method='POST')

    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(resp_json, status=200)

def auth(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)

    try:
        auth = request.POST["auth"]
    except KeyError as e:
        return HttpResponse(json.dumps({"error": "Key not found: " + e.args[0]}), status=400)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    post_data = {'authenticator': auth}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/check_authenticator', data=post_encoded, method='POST')

    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(resp_json, status=req.status_code)
