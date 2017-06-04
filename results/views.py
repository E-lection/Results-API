from django.http import HttpResponse


def index(request):
    return HttpResponse('Results API is online')
