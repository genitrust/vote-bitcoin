from django.contrib import admin
from votebitcoin.models import Candidate
from votebitcoin.models import VotingCard

admin.site.register(Candidate)

@admin.register(VotingCard)
class VotingCardAdmin(admin.ModelAdmin):
    search_fields = ['publicKey']
