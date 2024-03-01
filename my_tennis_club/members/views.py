from django.http import HttpResponse
from django.shortcuts import render

from .models import Member


# Create your views here.
def members(request):
    return HttpResponse(Member.objects.all())