from django.shortcuts import render
import urllib.request
from urllib.error import HTTPError
from django.http import HttpResponse
from django.urls import reverse

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
    # If we received a GET request instead of a POST request
    if request.method == 'GET':
        # display the login form page
        next = request.GET.get('next')
        return render(request, "login.html")

    # Creates a new instance of our login_form and gives it our POST data
    f = login_form(request.POST)

    # Check if the form instance is invalid
    if not f.is_valid():
      # Form was bad -- send them back to login page and show them an error
      return render('login.html', ...)

    # Sanitize username and password fields
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']

    # Get next page
    next = f.cleaned_data.get('next') or reverse('home')

    # Send validated information to our experience layer
    resp = login_exp_api(username, password)

    # Check if the experience layer said they gave us incorrect information
    if not resp or not resp['ok']:
      # Couldn't log them in, send them back to login page with error
      return render('login.html', ...)

    """ If we made it here, we can log them in. """
    # Set their login cookie and redirect to back to wherever they came from
    authenticator = resp['resp']['authenticator']

    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)

    return response
