from django.shortcuts import render
from django.template.context_processors import csrf

def csrf_provide(request):
    return render("<html><body></body></html>")
