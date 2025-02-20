import requests
import subprocess
import json
import os

from django.shortcuts import render
from django.conf import settings
from votebitcoin.models import Candidate
from votebitcoin.models import VotingCard


def vote(request):
    c = Candidate.objects.filter(active=True)
    print c
    return render(request, 'vote.html', {
        'candidates': c,
    })


class AddressPreviouslySpent(Exception):
    pass


class AddressEmpty(Exception):
    pass


class BlockChainDown(Exception):
    pass


def auditAddress(address):
    '''
    Audits to see whether or not the address has ever been used for sending
    coins. For our business requirements, a voting card is invalid and cannot
    be used if it had been used in the past to send coins.

    @param  string
    @raise  AddressPreviouslySpent
    @raise  AddressEmpty
    '''
    r = requests.get(
        'https://blockchain.info/address/%s?format=json' % address,
        verify=False
    )
    totalSent = r.json().get('total_sent', 0)
    try:
        # if totalSent is not in an expected format, then we'll consider
        # these coins as already spent.
        int(totalSent)
    except ValueError:
        raise AddressPreviouslySpent()
    if totalSent > 0:
        raise AddressPreviouslySpent()

    numberTxs = r.json().get('n_tx', 0)
    try:
        int(numberTxs)
    except ValueError:
        raise AddressEmpty()
    if numberTxs == 0:
        raise AddressEmpty()


def broadcast(signedHex):
    '''
    Broadcasts the signed transaction hex, returning True if the broadcast
    result was positive (successful).

    @param   string
    @return  bool
    '''
    try:
        r = requests.post(
            'https://blockchain.info/pushtx?api_code={}'
            .format(settings.BLOCKCHAIN_API_CODE),
            {
                'tx': signedHex,
                'api_code': settings.BLOCKCHAIN_API_CODE
            },
            verify=False
        )
    except:
        raise BlockChainDown()

    broadcastResult = r.text.strip()[:512]
    return broadcastResult == 'Transaction Submitted'


def results(request):
    return render(request, 'results.html', {
        'votes': VotingCard.objects.all().exclude(privateKey=None),
        'totalVotingCards': VotingCard.objects.all().count(),
        'candidates': Candidate.objects.filter(active=True),
    })


def submit(request):
    p = request.POST
    wif = p.get('voterWif', None)
    candidateKey = p.get('candidateVote', None)

    # Step 0: validate that both parameters were sent.
    if not wif or not candidateKey:
        return render(request, 'voting-invalid.html')

    # Step 1: convert wif to voting card's public key
    pk = None
    line = ['ku', wif, '--json']
    r = subprocess.Popen(line, shell=False, stdout=subprocess.PIPE)
    r = r.stdout.read()

    try:
        pk = json.loads(r).get('address_uncompressed')
        card = VotingCard.objects.get(publicKey=pk)
    except (ValueError, VotingCard.DoesNotExist):
        return render(request, 'voting-invalid.html')

    # Step 2: make sure the card has never been used for spending.
    try:
        auditAddress(pk)
    except ValueError:
        # at this point, if there's a ValueError, then no JSON object was
        # able to be decoded. Block chain must be down, or somehow an invalid
        # bitcoin address was used.
        return render(request, 'voting-invalid.html')
    except AddressEmpty:
        # whoops! somewhere, somebody forgot to distribute coins to this card!
        return render(request, 'vote-card-not-activated.html')
    except AddressPreviouslySpent:
        # this voting card is invalid...since the voting credit was removed!
        return render(request, 'vote-card-already-used.html')

    # Step 3: create, sign, and broadcast the transaction
    environment = (
        ('PYCOIN_CACHE_DIR', '%s/.pycoin_cache' % settings.BASE_DIR),
        ('PYCOIN_SERVICE_PROVIDERS',
            'BLOCKR_IO:BITEASY:BLOCKCHAIN_INFO:BLOCKEXPLORER'),
    )
    for (k, v) in environment:
        os.putenv(k, v)

    unsignedFile = '%s/.pycoin_cache/%s_%s.unsigned.hex' % (
        settings.BASE_DIR,
        pk,
        candidateKey,
    )
    line = ['tx', '-F', settings.VOTE_NETWORK_FEE, '-i', pk, candidateKey,
        '-o', unsignedFile]
    r = subprocess.call(line, shell=False, stdout=subprocess.PIPE)

    # Sign the transaction with voting card's wif
    signedFile = unsignedFile.replace('unsigned', 'signed')
    line = ['tx', unsignedFile, wif, '-o', signedFile]
    r = subprocess.call(line, shell=False, stdout=subprocess.PIPE)

    try:
        if not broadcast(file(signedFile).read()):
            return render(request, 'vote-card-already-used.html')
    except BlockChainDown:
        return render(request, 'voting-invalid.html')

    # Step 4: mark the voting card as used.
    card.privateKey = wif
    card.candidate = Candidate.objects.get(publicKey=candidateKey)
    card.save()
    return render(request, 'submit.html', {'candidate': card.candidate.name})
