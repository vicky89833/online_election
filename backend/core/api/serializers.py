from rest_framework import serializers
from voting import models
class CandidateTableSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.voterName', read_only=True)
    party_name = serializers.CharField(source='party.party', read_only=True)
    class Meta:
        model = models.CandidateTable
        fields = ['id', 'candidate_name', 'party_name'] 

class VoterTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoterTable
        fields = '__all__'