from optparse import make_option
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from votebitcoin.models import VotingCard
from votebitcoin.management.commands.distribute_votes import scrapeAddresses


class Command(BaseCommand):
    help = 'Imports voting cards from the Genitrust Note HTML document.'

    option_list = BaseCommand.option_list + (
        make_option('--html', dest='html',
                    help='Genitrust Notes Bulk HTML format.'),
    )

    def handle(self, *args, **options):
        alladdresses = scrapeAddresses(options['html'])
        count = 0
        for address in alladdresses:
            v = VotingCard()
            v.publicKey = address.string
            v.expiresOn = None
            try:
                v.save()
                count += 1
                self.stdout.write('Successfully imported Voting Card "%s"' % address)
            except IntegrityError:
                self.stdout.write('Ignoring Voting Card "%s"; '
                    'already imported!' % address)
        self.stdout.write('*** Imported a total of %d cards.' % count)
