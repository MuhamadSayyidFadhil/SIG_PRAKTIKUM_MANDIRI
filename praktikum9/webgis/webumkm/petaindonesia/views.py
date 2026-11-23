from django.http import HttpResponse
from django.shortcuts import render

def welcome(request):
    return HttpResponse("<h1>Selamat Datang di Situs Kami</h1>")
    # Create your views here.