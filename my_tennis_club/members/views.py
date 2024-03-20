from rest_framework import generics
from django.shortcuts import render

from .models import Member
from .serializers import MemberSerializer


class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    http_method_names = ['get']


class MemberCreateView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    http_method_names = ['post']