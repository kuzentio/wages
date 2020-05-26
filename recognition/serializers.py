from rest_framework import serializers

from recognition.models import RecogniseRequest


class RecogniseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecogniseRequest
        fields = ('image', )
