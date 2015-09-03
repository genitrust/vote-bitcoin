from django.contrib import admin
from votebitcoin.models import Candidate
from votebitcoin.models import VotingCard

admin.site.register(Candidate)
admin.site.register(VotingCard)
