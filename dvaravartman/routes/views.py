from django.shortcuts import render
from django.http import HttpResponse
import requests

proxies = {
   'http': '213.230.107.235:8080'
}
url = 'https://httpbin.org/ip'

# Create your views here.
def index(request):
    response = requests.get(url, proxies=proxies)
    return HttpResponse(response.text)
