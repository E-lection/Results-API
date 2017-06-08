from django.test import TestCase

from ..models import Vote
from ..counting_utils import get_candidates, count_votes, count_all_votes_for_constituency

CONSTITUENCY = "Richmond Park"
CONSTITUENCY_2 = "Brigg & Goole"
PARTY_1 = "Labour"
PARTY_2 = "Conservatives"
PARTY_3 = "UKIP"
PARTY_4 = "Liberal Democrats"
CAND_1_F_NAME = "Jeremy"
CAND_1_L_NAME = "Corbyn"
CAND_2_F_NAME = "Theresa"
CAND_2_L_NAME = "May"
CAND_3_F_NAME = "Paul"
CAND_3_L_NAME = "Nuttall"
CAND_4_F_NAME = "Tim"
CAND_4_L_NAME = "Farron"
CAND_1_VOTES = 12
CAND_2_VOTES = 7
CAND_3_VOTES = 2
CAND_4_VOTES = 4


CANDIDATES = [{'first_name': CAND_1_F_NAME,
               'last_name': CAND_1_L_NAME,
               'party': PARTY_1},
              {'first_name': CAND_2_F_NAME,
               'last_name': CAND_2_L_NAME,
               'party': PARTY_2},
              {'first_name': CAND_3_F_NAME,
               'last_name': CAND_3_L_NAME,
               'party': PARTY_3}]

CANDIDATES_AND_VOTES = [(CAND_1_VOTES, {'first_name': CAND_1_F_NAME,
                                        'last_name': CAND_1_L_NAME,
                                        'party': PARTY_1}),
                        (CAND_2_VOTES, {'first_name': CAND_2_F_NAME,
                                        'last_name': CAND_2_L_NAME,
                                        'party': PARTY_2}),
                        (CAND_3_VOTES, {'first_name': CAND_3_F_NAME,
                                        'last_name': CAND_3_L_NAME,
                                        'party': PARTY_3})]


def create_votes(number, constituency, party, candidate_first_name, candidate_last_name):
    for _ in range(number):
        Vote.objects.create(constituency=constituency,
                            party=party,
                            candidate_first_name=candidate_first_name,
                            candidate_last_name=candidate_last_name)


class CountingUtilsTests(TestCase):

    def setUp(self):
        create_votes(CAND_1_VOTES, CONSTITUENCY, PARTY_1,
                     CAND_1_F_NAME, CAND_1_L_NAME)
        create_votes(CAND_2_VOTES, CONSTITUENCY, PARTY_2,
                     CAND_2_F_NAME, CAND_2_L_NAME)
        create_votes(CAND_3_VOTES, CONSTITUENCY, PARTY_3,
                     CAND_3_F_NAME, CAND_3_L_NAME)
        create_votes(CAND_4_VOTES, CONSTITUENCY_2,
                     PARTY_4, CAND_4_F_NAME, CAND_4_L_NAME)

    def test_can_retrieve_list_of_distinct_candidates(self):
        candidates = get_candidates(CONSTITUENCY)

        self.assertEqual(candidates, CANDIDATES)

    def test_can_count_votes_for_a_candidate(self):
        votes = count_votes(CONSTITUENCY, {'first_name': CAND_1_F_NAME,
                                           'last_name': CAND_1_L_NAME,
                                           'party': PARTY_1})
        self.assertEqual(votes, CAND_1_VOTES)

    def test_counting_votes_for_constituency_returns_votes(self):
        (winner, votes, total_votes) = count_all_votes_for_constituency(CONSTITUENCY)

        self.assertEqual(winner, (CAND_1_VOTES, CANDIDATES[0]))
        self.assertEqual(votes, CANDIDATES_AND_VOTES)
        self.assertEqual(total_votes, CAND_1_VOTES + CAND_2_VOTES + CAND_3_VOTES)