from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import *
from voting import models
import json
import random
from twilio.rest import Client
from django.conf import settings
from .otp import send_otp_via_sms
from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, Sum,Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.core.exceptions import ObjectDoesNotExist

@api_view(['PUT'])
@permission_classes([AllowAny])
def otpGenerateView(request):
    if request.method=='PUT':
        votingID = request.data.get("voterId")
        print(votingID)
        voterDetail =None
        
 
        try:
            voterDetail= models.VoterTable.objects.get(voterId=votingID)
            print(voterDetail)
            
        except:
            voterDetail = None 
            return Response({"message":"Invalid voterId "}) 
        finally:
            
            if voterDetail.voted:
                return Response({"message":"already voted"})
            if str.lower(request.data.get("aadhar")) == str(voterDetail.aadhar):
                phone_number= "+91" +str(voterDetail.mobile)
                
                otp = send_otp_via_sms(phone_number)
                
                # data={"otp":otp}
                print(otp)
                data ={
                    "otp":otp,
                    "voterObj": voterDetail,
                    
                }
                cache.set(str(votingID), data, timeout=None)
                
                return Response({"message":"OTP Sent on Registered mobile number."})
            return Response({"message":"hisf"})
# { "voterId": "BR/05/302/378389","aadhar":"290634011234" }  

@api_view(['PUT'])
@permission_classes([AllowAny])
def otpVarifyView(request):
    if request.method =='PUT':

        otp= request.data.get("otp")
        votingID = request.data.get("voterId")
        print(otp)
        print(votingID)
        cached_data=cache.get(str(votingID))
        print(cached_data)
        if cached_data is not None and otp == cached_data.get("otp") :

            candidates_list = None
            voterObj=cached_data.get("voterObj")
            constituency_obj =voterObj.constituency
            constituencyId = constituency_obj.id
            candidates_list = cache.get(str(constituency_obj))
            if candidates_list is None:
                try:
                    candidates_list= models.CandidateTable.objects.filter(constituency=constituency_obj)
                    if candidates_list.exists():  
                        cache.set(str(constituency_obj), list(candidates_list), timeout=60 * 60*24)    
                except:
                    candidates_list = None 
                    return Response({"message":"Unknown constituency "}) 
                finally:
                    if candidates_list==None:
                        return Response({"message":"No candidates"})
                    
                    serializers= CandidateTableSerializer(candidates_list, many=True)
                    return Response({"candidates_list":serializers.data,"voterId":votingID})
            print("from cache")    
            serializers= CandidateTableSerializer(candidates_list, many=True)   
            return Response({"candidates_list":serializers.data,"voterId":votingID})    
        return Response({"message":"Invalid OTP"})        
#{"otp":"207454","voterId":"BR/05/302/378389"}          

@api_view(['PUT'])
@permission_classes([AllowAny])
def votingView(request):
    if request.method =='PUT':
        candidate=request.data.get("candidate")
        voterId = request.data.get("voterId")
        # print(candidate)

        #find who got vote
        candidateId= candidate.get("id")
        #voter object from cache
        voter_data=cache.get(str(voterId))
        if voter_data is None:
            return Response({"message":"session expired."})
        voterObj= voter_data.get("voterObj")
        if voter_data is None:
            return Response({"message":"session expired."})
        constituency= voterObj.constituency

        print(constituency)
        candidate_list=cache.get(str(constituency))
        candidate_obj=None
        for candidate in candidate_list:
           if str(candidate.id) == str(candidateId):
              candidate_obj= candidate
              break
           print(f"ID: {candidate.id}, Name: {candidate.candidate.voterName}")
        
        # candidate_obj = next((c for c in candidate_list if str(c.id) == str(candidateId)), None)
        print(candidateId)
        print(type(candidate_obj))
        print(type(voterObj))


        # print(f"{voterId} voted {candidate}")
        try:
            if voterObj.voted == True:
                return Response({"message":"already voted"})
            with transaction.atomic():
                
                vote= models.EVoteTable.objects.create(voter=voterObj,candidate=candidate_obj)
                
                voterObj.voted=True
                voterObj.save()
                
                    
                        
            return Response({"status": "success", "message": "Vote cast successfully", "vote_id": vote.id})
        
        except Exception as e:
            print(e)
            return Response({"message":"vote not cast"})
        

# {
#     "candidate": 
#         {
#             "id": "0f8c294d-6f5d-484a-8b90-3fccfe67038c",
#             "created_at": "2025-02-11T17:10:08.102585Z",
#             "constituency": "7e52d702-71a9-4b47-92ed-02498c75b795",
#             "party": "e8684e2e-c9d9-4850-a67d-a1422c345a0b",
#             "candidate": "57d8a37c-ae77-4797-b288-56eaec7ec8f2"
#         }
#     ,
#     "voterId": "BR/05/302/378389"
# }        
         

@api_view(['PUT'])
@permission_classes([AllowAny])
def AdminView(request):
    if request.method=='PUT':
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            try:
                if cache.get("voter_stats") is not None:
                    print("from cache")
                    return Response({"message":cache.get("voter_stats")})
                    
                voter_stats = (
                                models.VoterTable.objects.values("constituency__constituency_name")
                                .annotate(
                                    total_voters=Count("id"),
                                    voted_count=Count("id", filter=Q(voted=True)),
                                    not_voted_count=Count("id", filter=Q(voted=False)),
                                )
                                .order_by("constituency__constituency_name")  # Optional sorting
                            )
                
                cache.set("voter_stats", voter_stats, timeout=60)
                return Response({"message":voter_stats})
            except:
                return Response({"message":"Server is Occupiad. Try later"})
        return Response({"message":"UnAuthorized( Only for SuperUser)"})    
      

# { "username":"vicky","password":"123456"}      
