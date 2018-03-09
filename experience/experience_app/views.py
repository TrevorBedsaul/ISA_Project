from django.http import HttpResponse
import json
import urllib.request
from urllib.error import HTTPError


# Create your views here.

def book_detail(request, book_id):
    req = urllib.request.Request('http://models-api:8000/api/v1/books/' + str(book_id))

    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    return HttpResponse(resp_json, status=200)
