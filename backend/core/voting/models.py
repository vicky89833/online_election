from django.db import models
import uuid
from django.db.models import UniqueConstraint
class PartyTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    party = models.CharField(max_length=30, unique=True)
    created_at =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.party
    

class ParliamentaryConstituencyTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    constituency_name =models.CharField(max_length=30)
    district =models.CharField(max_length=30)
    state =models.CharField(max_length=30)
    created_at =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.constituency_name

    


class VoterTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voterId  = models.CharField(max_length=30, unique=True)
    voterName=  models.CharField(max_length=30)
    constituency = models.ForeignKey(ParliamentaryConstituencyTable, on_delete=models.CASCADE)
    aadhar = models.CharField(max_length=30,null=True)
    mobile = models.CharField(max_length=30)
    voted = models.BooleanField(default= False)
    created_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.voterName
    
class CandidateTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    constituency=models.ForeignKey(ParliamentaryConstituencyTable, on_delete=models.CASCADE)
    party=models.ForeignKey(PartyTable, on_delete=models.CASCADE)
    candidate = models.ForeignKey(VoterTable, on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.candidate.voterName
    

class EVoteTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # voter =models.ForeignKey(VoterTable, on_delete=models.CASCADE)
    voter = models.OneToOneField(VoterTable, on_delete=models.CASCADE)
    candidate= models.ForeignKey(CandidateTable, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voter} voted for {self.candidate}"
    
   




