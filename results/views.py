import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Vote
from .counting_utils import count_and_package_all_votes
from .api_utils import verify_pin_and_make_ineligible
from .api_key_verification import verify, has_vote_permissions

def index(request):
    return HttpResponse('Results API is online')

@csrf_exempt
@verify(lambda: has_vote_permissions)
def vote(request):
    if request.method == 'POST':
        vote_data = json.loads(request.body)

        if all (k in vote_data for k in ('constituency', 'party', 'first_name', 'last_name', 'pin_code', 'station_id')):
            constituency = vote_data['constituency']
            party = vote_data['party']
            candidate_first_name = vote_data['first_name']
            candidate_last_name = vote_data['last_name']
            pin_code = vote_data['pin_code']
            station_id = vote_data['station_id']

            if verify_pin_and_make_ineligible(station_id, pin_code):
                if constituency and party and candidate_last_name and candidate_first_name:
                    vote_object = Vote(constituency=constituency,
                                       party=party,
                                       candidate_first_name=candidate_first_name,
                                       candidate_last_name=candidate_last_name)
                    vote_object.save()
                    return JsonResponse({'success': True,
                                         'error' : None})

            return JsonResponse({'success': False,
                                 'error' : 'Voter is ineligible'})


    return JsonResponse({'success': False,
                         'error' : 'Missing input data'})

@csrf_exempt
def vote_script(request):
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
                return JsonResponse({'success': True,
                                     'error' : None})



    return JsonResponse({'success': False,
                         'error' : 'Missing input data'})

def delete_votes(request):
    Vote.objects.all().delete()
    return JsonResponse({'success' : True})


def outcome(request):
    map_data, overall_data = count_and_package_all_votes()
    return JsonResponse({'map_data': map_data, 'overall_data': overall_data})
