from rest_framework import serializers
from voting import models
class CandidateTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CandidateTable
        fields = '__all__'

class VoterTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoterTable
        fields = '__all__'