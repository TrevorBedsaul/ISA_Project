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
    seller_req = urllib.request.Request('http://models-api:8000/api/v1/sellers/' + str(seller_id))
    try:
        seller_json = urllib.request.urlopen(seller_req).read().decode('utf-8')
        if has_buyer:
            buyer_req = urllib.request.Request('http://models-api:8000/api/v1/buyers/' + str(book['buyer']))
            buyer_json = urllib.request.urlopen(buyer_req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    seller = json.loads(seller_json)
    book['seller'] = {'id':seller['id'], 'name':seller['generic_user']['name']}
    if has_buyer:
        buyer = json.loads(buyer_json)
        book['buyer'] = {'id': buyer['id'], 'name': buyer['generic_user']['name']}
    return HttpResponse(json.dumps(book), status=200)
