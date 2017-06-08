import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Vote
from .counting_utils import count_and_package_all_votes

def index(request):
    return HttpResponse('Results API is online')

@csrf_exempt
def vote(request):
    if request.method == 'POST':
        vote_data = json.loads(request.body)

        if all (k in vote_data for k in ('constituency', 'party', 'first_name', 'last_name')):
            constituency = vote_data['constituency']
            party = vote_data['party']
            candidate_first_name = vote_data['first_name']
            candidate_last_name = vote_data['last_name']

            if constituency and party and candidate_last_name and candidate_first_name:
                vote_object = Vote(constituency=constituency,
                                   party=party,
                                   candidate_first_name=candidate_first_name,
                                   candidate_last_name=candidate_last_name)
                vote_object.save()
                return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def outcome(request):
    votes = count_and_package_all_votes()
    return  JsonResponse( {'map_data' : votes} )
