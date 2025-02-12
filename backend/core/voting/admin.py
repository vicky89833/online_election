from django.contrib import admin


from .models import *

admin.site.register(ParliamentaryConstituencyTable)
admin.site.register(CandidateTable)
admin.site.register(VoterTable)
admin.site.register(EVoteTable)
admin.site.register(PartyTable)  
