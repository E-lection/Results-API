import json

from django.test import TestCase
from django.urls import reverse

from ..models import Vote

CONSTITUENCY = "Chelsea and Fulham"
PARTY = "Conservative"
CAND_FIRST_NAME = "Theresa"
CAND_LAST_NAME = "May"

RESPONSE_OK = 200

class PostVoteTestCases(TestCase):

    def test_endpoint_returns_repsonse(self):
        url = reverse('results:vote')
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'success': False})

    def test_post_vote_adds_vote(self):
        post_data = {
            'constituency': CONSTITUENCY,
            'party': PARTY,
            'candidate_first_name': CAND_FIRST_NAME,
            'candidate_last_name': CAND_LAST_NAME
        }
        url = reverse('results:vote')

        response = self.client.post(url,
                                    json.dumps(post_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'success': True})

        vote = Vote.objects.get(constituency=CONSTITUENCY)
        self.assertIsNotNone(vote)
        self.assertEqual(vote.constituency, CONSTITUENCY)
        self.assertEqual(vote.party, PARTY)
        self.assertEqual(vote.candidate_first_name, CAND_FIRST_NAME)
        self.assertEqual(vote.candidate_last_name, CAND_LAST_NAME)
