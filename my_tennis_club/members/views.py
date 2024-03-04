import json

from django.http import HttpResponse
from django.shortcuts import render

from .models import Member


# Create your views here.
def members(request):
    members = Member.objects.all().values()
    json_data = json.dumps(list(members))
    return HttpResponse(json_data)