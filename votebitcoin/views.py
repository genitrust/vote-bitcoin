from django.shortcuts import render


def vote(request):
    return render(request, 'vote.html')


def submit(request):
    return render(request, 'submit.html')
