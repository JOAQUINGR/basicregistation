from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def home(request):
    return render(request, template_name="website/home.html")
