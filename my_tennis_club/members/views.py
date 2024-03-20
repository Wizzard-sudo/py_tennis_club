from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from rest_framework import generics
from django.shortcuts import render

from .models import Member
from .serializers import MemberSerializer


class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    http_method_names = ['get']


def get_member_by_id(request, id):
    if Member.objects.filter(id=id).exists():
        data = MemberSerializer(Member.objects.get(id=id)).data
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotFound(f'Member with id %s not found' % id)


class MemberCreateView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    http_method_names = ['post']
