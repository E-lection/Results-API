from .models import Vote

# Retrieves the candidates in the constituency


def get_candidates(constituency):
    candidates = []
    # Get the distinct values in the party field for the given constituency
    parties = Vote.objects.filter(
        constituency=constituency).values('party').distinct()

    for party in parties:
        candid = Vote.objects.filter(party=party['party']).filter(constituency=constituency)
        candidate = {'first_name': candid[0].candidate_first_name,
                     'last_name': candid[0].candidate_last_name,
                     'party': party['party']}
        candidates.append(candidate)

    return candidates


def count_votes(constituency, candidate):
    return Vote.objects.filter(constituency=constituency,
                               candidate_first_name=candidate['first_name'],
                               candidate_last_name=candidate['last_name'],
                               party=candidate['party']).count()


def count_all_votes_for_constituency(constituency):
    candidates = get_candidates(constituency)
    total_votes = 0
    winning_votes = 0
    winner = None
    results = []

    for candidate in candidates:
        votes = count_votes(constituency, candidate)
        total_votes += votes
        results.append({'votes': votes, 'candidate': candidate})
        if votes > winning_votes:
            winning_votes = votes
            winner = candidate

    return ((winning_votes, winner), results, total_votes)


def count_and_package_all_votes():
    constituencies = Vote.objects.values('constituency').distinct()
    map_data = []
    overall_data = {
        'votes_counted': 0,
        'parties': [],
    }

    for constituency in constituencies:
        ((winning_votes, winner), votes, total_votes) = count_all_votes_for_constituency(
            constituency['constituency'])
        result = {'constituency': constituency['constituency'],
                  'winning_candidate': winner,
                  'winning_votes': winning_votes,
                  'total_votes': total_votes,
                  'votes': votes}
        map_data.append(result)

        overall_data['votes_counted'] += total_votes

        for candidate_votes in votes:
            party_name = candidate_votes['candidate']['party']
            if not any(d['party'] == party_name for d in overall_data['parties']):
                party = {
                    'party': party_name,
                    'seats': 0,
                    'votes': 0,
                    'vote_share': 0
                }
                overall_data['parties'].append(party)

            party_data = filter(lambda party: party['party'] == party_name, overall_data['parties'])[0]
            if winner['party'] == party_name:
                party_data['seats'] += 1
            party_data['votes'] += candidate_votes['votes']

    for party in overall_data['parties']:
        total_votes = overall_data['votes_counted']

        party_votes_share = (float(party['votes']) / float(total_votes)) * 100
        party['vote_share'] = party_votes_share

    return (map_data, overall_data)
