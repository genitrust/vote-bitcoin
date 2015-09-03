from django.db import models


class Candidate(models.Model):
    '''
    The candidate to receive votes. Candidates cannot receive a vote if the
    "vote" spend is not previously registered as a Voting Card.
    '''

    name = models.CharField(max_length=32)
    active = models.BooleanField(default=True)
    publicKey = models.CharField(max_length=35, unique=True,
        help_text='Should be unused.')

    def __unicode__(self):
        msg = self.name
        if not self.active:
            msg += ' (inactive)'
        return msg


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
    privateKey = models.CharField(max_length=52, null=True, blank=True,
        default=None)
    candidate = models.ForeignKey(Candidate, null=True, blank=True,
        default=None)

    def __unicode__(self):
        msg = 'Voting Card: %s' % self.publicKey
        if self.used():
            msg += ' (redeemed)'
        return msg

    def used(self):
        return bool(self.privateKey)
