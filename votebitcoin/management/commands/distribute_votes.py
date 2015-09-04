from optparse import make_option
from bs4 import BeautifulSoup
import subprocess
import os
from django.core.management.base import BaseCommand, CommandError
from votebitcoin.models import VotingCard


def scrapeAddresses(htmlFile):
    soup = BeautifulSoup(open(htmlFile), 'html.parser')
    addresses = soup.findAll('div', {'class': 'btcaddress'})
    return [x.string for x in addresses]

class Command(BaseCommand):
    help = 'Outputs the signed transaction hex for broadcasting ' + \
        '(distributing) coins to all Vote Cards.'

    option_list = BaseCommand.option_list + (
        make_option('--html', dest='html',
            help='Genitrust Notes Bulk HTML format -- all files separated '
            'by commas.'),
        make_option('--input', dest='input',
            help='Source of bitcoin as the input address.'),
        make_option('--size', dest='size', type=str,
            help='Distribution size in units (satoshi) per Vote Card.'),
        make_option('--wif', dest='wif',
            help='The input public key\'s corresponding private key for '
            'signing the bitcoin transaction.'),
        make_option('--change', dest='change',
            help='Change address to send the remaining voting credits.'),
    )

    def handle(self, *args, **options):
        self.stdout.write('html: %s' % options['html'].split(','))
        self.stdout.write('input: %s' % options['input'])
        self.stdout.write('size: %s' % options['size'])
        self.stdout.write('wif: %s' % options['wif'])
        self.stdout.write('change: %s' % options['change'])

        htmlFiles = options['html'].split(',')
        inputCoins = options['input']
        unitSize = options['size']
        signingWif = options['wif']
        changeAddress = options['change']

        # STEP 1: load all of the voting card bitcoin addresses from HTML files
        btcAddresses = []
        for htmlFile in htmlFiles:
            # TODO: use a function here to scrape the stuff.
            # this function should return a list of bitcoin addresses!!!
            btcAddresses += scrapeAddresses(htmlFile)
            #pass

        # STEP 2: build the transaction with all bitcoin addresses as the
        # transaction outputs.
        line = ['tx', '-i', inputCoins]
        # add each voting card bitcoin address to the command 'line', followed
        # by the amount of satoshi units.
        for address in btcAddresses:
            line += ['%s/%s' % (address, unitSize)]
        line += [changeAddress]
        # output of the unsigned transaction hex
        unsignedTxFile = '%s_%s.unsigned.tx' % (inputCoins, changeAddress)
        line += ['-o', unsignedTxFile]

        # STEP 3: finally -- build the transaction!
        # TODO:
        # use Popen to run this baby? maybe a better solution since we do not
        # need the text from the transaction creation...
        #self.stdout.write('Command for building the transaction: {}'.format(
        #    ' '.join(line)
        #))
        environment = (
                  ('PYCOIN_CACHE_DIR', '~/.pycoin_cache'),
                  ('PYCOIN_SERVICE_PROVIDERS', 'BLOCKR_IO:BITEASY:BLOCKEXPLORER'),
               )
        for (k, v) in environment:
            os.putenv(k, v)

        subprocess.call(line, shell=False, stdout=subprocess.PIPE)
        # STEP 4: sign the transaction, with the output going directly to
        # standard output.
        signedTxFile = str(unsignedTxFile).replace('unsigned', 'signed')
#        line.pop()
        line = ['tx', str(unsignedTxFile), signingWif, '-o', signedTxFile]
        # TODO: send the 'line' to the system command line, and allow the output
        # to be displayed on the screen.
        #print subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE).stdout.read() 
        subprocess.call(line, shell=False, stdout=subprocess.PIPE)
        #print result
        line = ['tx', signedTxFile]
        result = []
        result = subprocess.Popen(line, shell=False, stdout=subprocess.PIPE)
        with result.stdout as f:
            output = f.read()
        return output
