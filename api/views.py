# coding: utf-8
import logging

from django.shortcuts import render
from rest_framework import viewsets

from api.models import User
from api.serializers import UserSerializer

log = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def start_page(request, title="Simple Django RESTFull ToDo App"):
    """Home page view"""
    content = {'title': title}
    return render(request, 'index.html', content)
