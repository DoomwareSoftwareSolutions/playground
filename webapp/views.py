#!/usr/bin/env python
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

def BaseView(request):
    if request.method == 'GET':
        return render_to_response('index.html',{},RequestContext(request))
    else:
        pass # TODO POST METHOD