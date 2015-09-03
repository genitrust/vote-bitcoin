from django.core.management.base import BaseCommand, CommandError
from votebitcoin.models import VotingCard

class Command(BaseCommand):
    help = 'Imports voting cards from the Genitrust Note HTML document.'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_id', nargs='+', type=int)
    def add_arguments(self, parser):
        parser.add_argument('--html', type=str)
	

    def handle(self, *args, **options):
        import sys
        from bs4 import BeautifulSoup
#        soup = BeautifulSoup(open("notes_101-200.html"))
        #self.stdout.write('you supplied the html option:', options['html'])
        soup = BeautifulSoup(open(options['html']),"html.parser")
        
#        sys.stdout = open('outputt2', 'w')
        
        alladdresses = soup.findAll('div',{'class':'btcaddress'})
        for address in alladdresses:
            v = VotingCard()
            v.publicKey = address
            v.expiresOn = None
            v.save()
            self.stdout.write('Successfully imported Voting Card "%s"' % address)
