from django.shortcuts import render
from rest_framework import viewsets

from recognition.models import RecogniseRequest
from recognition.serializers import RecogniseRequestSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RecogniseRequestSerializer
    queryset = RecogniseRequest.objects.all()
