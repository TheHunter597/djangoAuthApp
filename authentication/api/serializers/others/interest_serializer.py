from ....models import Interest
from rest_framework import serializers


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ["id", "name"]
