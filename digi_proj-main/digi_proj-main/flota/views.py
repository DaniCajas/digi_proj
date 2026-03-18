from django.shortcuts import render

def inicio(request):
    # En lugar de un HttpResponse, usamos 'render' para cargar el archivo HTML
    return render(request, 'flota/inicio.html')
