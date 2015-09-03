from django.shortcuts import render
from votebitcoin.models import Candidate
from votebitcoin.models import VotingCard


def vote(request):
    c = Candidate.objects.filter(active=True)
    print c
    return render(request, 'vote.html', {
        'candidates': c,
    })


def submit(request):
    p = request.POST
    wif = p.get('wif', None)
    candidateKey = p.get('candidateKey', None)

    # Step 0: validate that both parameters were sent.
    if not wif or not candidateKey:
        return render(request, 'voting-error.html')

    # Step 1: convert wif to voting card's public key
    # tx wif --json
    # grab the response's address_uncompressed property.
    pk = None
    try:
        card = VotingCard.objects.get(publicKey=pk)
    except VotingCard.DoesNotExist:
        return render(request, 'voting-error.html')

    # Step 2: create, sign, and broadcast the transaction
    # tx -F 5000 -i pk candidateKey -o file ... only if file is necessary!
    # tx file wif
    # electrum sendrawtransaction (???) hexHere
    # or use blockchain.info -- since we're used to that ;) scary idea tho!
    # result = result.

    # if anything other than a positive message comes back, cannot vote!
    positiveResult = True
    if not positiveResult:
        return render(request, 'voting-error.html')

    # Step 3: mark the voting card as used.
    card.privateKey = wif
    card.candidate = Candidate(candidate)
    card.save()

    print 'candidate:', request.POST.get('candidate', 'heh')
    return render(request, 'submit.html')
