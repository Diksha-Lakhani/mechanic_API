from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Mechanic, ServiceRequest
from .serializers import MechanicSerializer, ServiceRequestSerializer

#inherts the HTTP protocols(get/post/put/patch/delete) from ModelViewSet class
class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
