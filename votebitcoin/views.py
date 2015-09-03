from django.shortcuts import render
from votebitcoin.models import Candidate


def vote(request):
    c = Candidate.objects.filter(active=True)
    print c
    return render(request, 'vote.html', {
        'candidates': c,
    })


def submit(request):
    print 'candidate:', request.POST.get('candidate', 'heh')
    return render(request, 'submit.html')
