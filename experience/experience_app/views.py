from django.http import HttpResponse
import json
import urllib.request
from urllib.error import HTTPError
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

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


    auth = request.COOKIES.get('auth')

    post_data = {'authenticator': auth}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    auth_req = urllib.request.Request('http://localhost:8000/api/v1/check_authenticator', data=post_encoded, method='POST')

    is_logged_in = True
    try:
        response = urllib.request.urlopen(auth_req).read().decode('utf-8')
        response_json = json.loads(response)
        user_id = response_json["user_id"]
    except Exception as e:
        is_logged_in = False

    if is_logged_in:
        pageview_info = {"user_id": user_id, "book_id": book_id}
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('pageview-topic', json.dumps(pageview_info).encode('utf-8'))

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

        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/books/create', data=post_encoded, method='POST')

        try:
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        except HTTPError as e:
            return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
        except Exception as e:
            return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

        producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
        producer.send('new-listings-topic', resp_json.encode('utf-8'))

        return HttpResponse(resp_json, status=201)
    else:
        return HttpResponse(json.dumps({"error":"incorrect method (use GET or POST instead)"}), status=405)

def create_user(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({}), status=200)

    elif request.method == "POST":
        post_data = request.POST

        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/users/create', data=post_encoded, method='POST')

        try:
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        except HTTPError as e:
            return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
        except Exception as e:
            return HttpResponse(json.dumps({"error": str(type(e))}), status=500)
        return HttpResponse(resp_json, status=201)
    else:
        return HttpResponse(json.dumps({"error":"incorrect method (use GET or POST instead)"}), status=405)


def search(request):
    if request.method == "POST":
        return HttpResponse(json.dumps({}), status=200)

    elif request.method == "GET":
        query = request.GET.get('query', 'none')

        es = Elasticsearch(['es'])

        result = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 5})

        if result['timed_out'] == True:
            return HttpResponse(json.dumps({"error":"Search timed out"}), status=500)

        sources = []
        for returned in result['hits']['hits']:
            sources.append(returned['_source'])

        return HttpResponse(json.dumps(sources), status=201)

    else:
        return HttpResponse(json.dumps({"error":"incorrect method (use GET or POST instead)"}), status=405)

def get_recommendation(request, book_id):
    book_rec = urllib.request.Request('http://models-api:8000/api/v1/books/recommendation')

    try:
        rec_json = urllib.request.urlopen(book_rec).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponse(json.dumps({"error": e.msg}), status=e.code)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(type(e))}), status=500)

    reco_list = json.loads(rec_json)

    for book in reco_list:
        if book['item_id'] == book_id:
            rec_items = book['recommended_items'].split(',')
            recs = list(map(int, rec_items))
            list_rec = []
            for i in recs:
                try:#list_rec.append(urllib.request.Request.get('http://models-api:8000/api/v1/meme_item/' + str(i) + '/').json())
                    list_rec.append(urllib.request.Request('http://models-api:8000/api/v1/books?id=' + str(i)))
                except:
                    return HttpResponse(json.dumps({"error": "Book not found"}), status=404)

    return HttpResponse(json.dumps(list_rec), status=200)
