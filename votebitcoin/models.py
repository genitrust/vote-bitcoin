from django.db import models

class Candidate(models.Model):
    '''
    The candidate to receive votes. Candidates cannot receive a vote if the
    "vote" spend is not previously registered as a Voting Card.
    '''

    name = models.CharField(max_length=32)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        msg = self.name
        if not self.active:
            msg += ' (inactive)'
        return msg

    def publicKey(self):
        '''
        This is where coins must be sent to the candidate in order for the
        candidate to be considered voted for.
        '''
        pass


class VotingCard(models.Model):
    '''
    Voting Cards are distributed to people. Any of these voting cards can be
    used to vote AS LONG AS:

    * The public key is discovered to contain a bitcoin
    * The public key has *NEVER* been spent previously.
    '''

    createdOn = models.DateTimeField(auto_now_add=True)
    expiresOn = models.DateTimeField(null=True)
    publicKey = models.CharField(max_length=35, unique=True)
    used = models.BooleanField(default=False)
