from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseForbidden

def index(request):
    return render(request, 'application/main.html')