from django.shortcuts import render
import urllib.request
from urllib.error import HTTPError
from django.http import HttpResponse
import json

# Create your views here.
def home(request):
    req = urllib.request.Request('http://exp-api:8000/api/v1/home')
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    book_list = json.loads(resp_json)
    return render(request, "home.html", {"book_list":book_list})
