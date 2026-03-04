from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("<h1>¡Bienvenido a Dakkar Car Rental!</h1> <p>Esta será la página principal de nuestra flota.</p>")
# Create your views here.
