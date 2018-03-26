from django.http import HttpResponse
import json
import urllib.request
from urllib.error import HTTPError


# Create your views here.

def home(request):
    req = urllib.request.Request('http://models-api:8000/api/v1/books')
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(resp_json, status=200)


def book_detail(request, book_id):
    book_req = urllib.request.Request('http://models-api:8000/api/v1/books?id=' + str(book_id))

    try:
        book_json = urllib.request.urlopen(book_req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    book_list = json.loads(book_json)
    if len(book_list) != 1:
        return HttpResponse(json.dumps({"error": "Book not found"}), status=404)
    book = book_list[0]
    seller_id = book['seller']
    has_buyer = (book['buyer'] != None)

    seller_req = urllib.request.Request('http://models-api:8000/api/v1/users?id=' + str(seller_id))
    try:
        seller_json = urllib.request.urlopen(seller_req).read().decode('utf-8')
        if has_buyer:
            buyer_req = urllib.request.Request('http://models-api:8000/api/v1/users?id=' + str(book['buyer']))
            buyer_json = urllib.request.urlopen(buyer_req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    seller_list = json.loads(seller_json)
    if len(seller_list) != 1:
        return HttpResponse(json.dumps({"error": "Seller not found"}), status=404)
    seller = seller_list[0]
    book['seller'] = {'id':seller['id'], 'name':seller['name']}
    if has_buyer:
        buyer_list = json.loads(buyer_json)
        if len(buyer_list) != 1:
            return HttpResponse(json.dumps({"error": "Buyer not found"}), status=404)
        buyer = buyer_list[0]
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

def check_authenticator(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)

    try:
        auth = request.POST["authenticator"]
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
    return HttpResponse(resp_json, status=urllib.request.urlopen(req).getcode())

def logout(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"error":"incorrect method (use POST instead)"}), status=405)

    try:
        auth = request.POST["authenticator"]
    except KeyError as e:
        return HttpResponse(json.dumps({"error": "Key not found: " + e.args[0]}), status=400)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    post_data = {'authenticator': auth}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/logout', data=post_encoded, method='POST')

    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
    return HttpResponse(resp_json, status=200)

def create_listing(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({}), status=200)

    elif request.method == "POST":
        post_data = request.POST
        #return HttpResponse(json.dumps(post_data), status=200)

        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/books/create', data=post_encoded, method='POST')

        try:
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        except HTTPError as e:
            return HttpResponse(json.dumps({"error": e.msg, "response":resp_json}), status=e.code)
        except Exception as e:
            return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
        return HttpResponse(resp_json, status=201)
    else:
        return HttpResponse(json.dumps({"error":"incorrect method (use GET or POST instead)"}), status=405)
