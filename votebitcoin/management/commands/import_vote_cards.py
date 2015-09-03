from optparse import make_option
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError
from votebitcoin.models import VotingCard

class Command(BaseCommand):
    help = 'Imports voting cards from the Genitrust Note HTML document.'

    option_list = BaseCommand.option_list + (
        make_option('--html', dest='html',
                    help='Genitrust Notes Bulk HTML format.'),
    )

    def handle(self, *args, **options):
#        soup = BeautifulSoup(open("notes_101-200.html"))
        self.stdout.write('you supplied the html option: %s' % options['html'])
        soup = BeautifulSoup(open(options['html']),"html.parser")

        alladdresses = soup.findAll('div', {'class':'btcaddress'})
        for address in alladdresses:
            v = VotingCard()
            v.publicKey = address
            v.expiresOn = None
            v.save()
            self.stdout.write('Successfully imported Voting Card "%s"' % address)
