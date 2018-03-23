from django.shortcuts import render
import urllib.request
from urllib.error import HTTPError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm

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

def book_detail(request, book_id):
    req = urllib.request.Request('http://exp-api:8000/api/v1/books/' + str(book_id))
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    book = json.loads(resp_json)
    return render(request, "book_detail.html", {"book":book})

def login(request):

    if request.method == 'GET':
        form = LoginForm()
        context = {"form": form}
        return render(request, "login.html", context)

    f = LoginForm(request.POST)

    # Check if the form instance is invalid
    if not f.is_valid():
      ## TODO Form was bad -- send them back to login page and show them an error
      context = {"form": f, "error": "Form was invalid"}
      return render(request, 'login.html', context)


    username = f.cleaned_data['username']
    password = f.cleaned_data['password']

    post_data = {'username': username, 'password': password}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/v1/login', data=post_encoded, method='POST')

    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        ## TODO Form was bad -- send them back to login page and show them an error
        context = {"form": f, "error": "HTTP error: " + e.msg}
        return render(request, 'login.html', context)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    resp_dict = json.loads(resp_json)
    authenticator = resp_dict['authenticator']
    response = HttpResponseRedirect("")
    response.set_cookie("auth", authenticator)
    return response
