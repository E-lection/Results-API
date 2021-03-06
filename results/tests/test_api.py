import json

from django.test import TestCase
from django.urls import reverse

from ..models import Vote

CONSTITUENCY = "Chelsea and Fulham"
PARTY = "Conservative"
CAND_FIRST_NAME = "Theresa"
CAND_LAST_NAME = "May"

RESPONSE_OK = 200
RESPONSE_UNAUTHORIZED = 401

PARTY_1 = "Labour"
PARTY_2 = "Conservatives"
PARTY_3 = "UKIP"
CAND_1_F_NAME = "Jeremy"
CAND_1_L_NAME = "Corbyn"
CAND_2_F_NAME = "Theresa"
CAND_2_L_NAME = "May"
CAND_3_F_NAME = "Paul"
CAND_3_L_NAME = "Nuttall"
CAND_1_VOTES = 12
CAND_2_VOTES = 7
CAND_3_VOTES = 2
TOT_VOTES = CAND_1_VOTES + CAND_2_VOTES + CAND_3_VOTES

CANDIDATE_1 = {'first_name': CAND_1_F_NAME,
               'last_name': CAND_1_L_NAME,
               'party': PARTY_1}
CANDIDATE_2 = {'first_name': CAND_2_F_NAME,
               'last_name': CAND_2_L_NAME,
               'party': PARTY_2}
CANDIDATE_3 = {'first_name': CAND_3_F_NAME,
               'last_name': CAND_3_L_NAME,
               'party': PARTY_3}

PARTY_DATA_1 = {'party': PARTY_1,
                'votes': CAND_1_VOTES,
                'vote_share': (float(CAND_1_VOTES) / TOT_VOTES) * 100,
                'seats': 1}

PARTY_DATA_2 = {'party': PARTY_2,
                'votes': CAND_2_VOTES,
                'vote_share': (float(CAND_2_VOTES) / TOT_VOTES) * 100,
                'seats': 0}

PARTY_DATA_3 = {'party': PARTY_3,
                'votes': CAND_3_VOTES,
                'vote_share': (float(CAND_3_VOTES) / TOT_VOTES) * 100,
                'seats': 0}

RESULTS_JSON = {'map_data': [
               {'constituency': CONSTITUENCY,
                'winning_candidate': CANDIDATE_1,
                'winning_votes': CAND_1_VOTES,
                'total_votes': CAND_1_VOTES + CAND_2_VOTES + CAND_3_VOTES,
                'votes': [
                    {'candidate': CANDIDATE_1, 'votes': CAND_1_VOTES},
                    {'candidate': CANDIDATE_2, 'votes': CAND_2_VOTES},
                    {'candidate': CANDIDATE_3, 'votes': CAND_3_VOTES},
                ]}],
                'overall_data': {
                    'votes_counted': CAND_1_VOTES + CAND_2_VOTES + CAND_3_VOTES,
                    'parties': [
                        PARTY_DATA_1, PARTY_DATA_2, PARTY_DATA_3
                    ]
                }}


def create_votes(number, constituency, party, candidate_first_name, candidate_last_name):
    for _ in range(number):
        Vote.objects.create(constituency=constituency,
                            party=party,
                            candidate_first_name=candidate_first_name,
                            candidate_last_name=candidate_last_name)


class PostVoteTestCases(TestCase):

    def test_endpoint_returns_repsonse(self):
        url = reverse('results:vote')
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_UNAUTHORIZED)


class OutcomeMapDataTests(TestCase):

    def setUp(self):
        create_votes(CAND_1_VOTES, CONSTITUENCY, PARTY_1,
                     CAND_1_F_NAME, CAND_1_L_NAME)
        create_votes(CAND_2_VOTES, CONSTITUENCY, PARTY_2,
                     CAND_2_F_NAME, CAND_2_L_NAME)
        create_votes(CAND_3_VOTES, CONSTITUENCY, PARTY_3,
                     CAND_3_F_NAME, CAND_3_L_NAME)

    def test_endpoint_returns_repsonse(self):
        url = reverse('results:outcome')
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    def test_can_retrieve_results(self):
        url = reverse('results:outcome')
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, RESULTS_JSON)
