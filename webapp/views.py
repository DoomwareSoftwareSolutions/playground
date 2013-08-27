#!/usr/bin/env python
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

def baseview(request):
    return render_to_response('index.html',{},RequestContext(request))

def signupview(request):
    return render_to_response('signup.html',{},RequestContext(request))