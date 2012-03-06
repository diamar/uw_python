# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from mybooks.models import Poll
from django.http import Http404
from django.http import HttpResponse


def index(request):
    latest_poll_list = Poll.objects.all().order_by('bkid')
    return render_to_response('mybooks/index.html', {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('mybooks/detail.html', {'poll': p})

#def detail(request, poll_id):
#    return HttpResponse("You're looking at poll %s." % poll_id)
