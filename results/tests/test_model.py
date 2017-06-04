from django.test import TestCase

from ..models import Vote

def create_vote():
    return Vote(constituency='Kensington',
                party='Labour',
                candidate_first_name='Jeremy',
                candidate_last_name='Corbyn')

class VoteModelTests(TestCase):

    def test_string_representation(self):
        vote = create_vote()
        self.assertEqual(str(vote), 'Kensington - Labour - Corbyn')
