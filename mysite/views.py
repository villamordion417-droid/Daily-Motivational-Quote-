from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods

# Create your views here.

@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint"""
    return HttpResponse("OK", status=200)

def index(request):
    return HttpResponse("This is index page")