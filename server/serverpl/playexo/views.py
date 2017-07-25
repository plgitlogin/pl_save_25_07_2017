#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python [Version]
#
#  Author: Coumes Quentin     Mail: qcoumes@etud.u-pem.fr
#  Created: 2017-07-05
#  Last Modified: 2017-07-05

import json, logging

from sympy import evaluate

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template import Context, Template
from django.contrib import messages

from serverpl.settings import MEDIA_ROOT

from gitload.models import PLTP, PL, Strategy

from sandbox.models import Sandbox

from playexo.pythonbuildertest import PythonBuilderTest
from playexo.exercise import Exercise, ExerciseTest
from playexo.builder import PythonBuilder, PythonBuilderTest
from playexo.models import Activity, Answer

from pysrc.plrequest import SandboxSession


@csrf_exempt
@login_required
def activity_view(request):
    activity_name = request.session.get("current_activity", None)
    exercise = request.session.get("exercise", None)
    pl_sha1 = None
    success = None
    feedback = None
    
    if exercise:
        exercise = Exercise(exercise)
        
    if request.method == 'GET' or request.method == 'POST':
        action = request.GET.get("action", None)
        if action == "pl":
            pl_sha1 = request.GET.get("pl_sha1", None)
        elif action == "pltp":
            exercise = None
            request.session["exercise"] = None
        status = None
        
        try:
            status = json.loads(request.body.decode())
        except:
            pass
        if status and status['requested_action'] == 'submit' :
            success, feedback = exercise.evaluate(status['inputs'])
            if 'answer' in status['inputs']:
                value = status['inputs']['answer']
            else:
                value = ""
            if success:
                Answer(value=value, user=request.user, pl=PL.objects.get(sha1=exercise.dic['pl_sha1']), seed=exercise.dic['seed'], state=Answer.SUCCEEDED).save()
            else:
                Answer(value=value, user=request.user, pl=PL.objects.get(sha1=exercise.dic['pl_sha1']), seed=exercise.dic['seed'], state=Answer.FAILED).save()
            return HttpResponse(json.dumps({'success': success, 'feedback': feedback}), content_type='application/json')
            
    if not exercise or pl_sha1:
        activity = Activity.objects.get(name=activity_name)
        pl = None
        if pl_sha1:
            pl = PL.objects.get(sha1=pl_sha1)
        exercise = PythonBuilder(request, activity, pl).get_exercise()
        if pl_sha1:
            try:
                Answer.objects.filter(user=request.user, pl=pl)[0]
            except:
                Answer(value="", user=request.user, pl=pl, seed=exercise.dic['seed']).save()
            request.session['exercise'] = exercise.dic
            return redirect(activity_view) #Remove get parameters from url
            
    request.session['exercise'] = exercise.dic
    return HttpResponse(exercise.render(request, feedback, success))
    

@login_required
@csrf_exempt
def lti_receiver(request, activity_name, strategy_name, pltp_sha1):
    activity_id = request.session.pop("activity", None)
    if not activity_id:
        raise Http404
    
    try:
        activity = Activity.objects.get(id=activity_id)
    except:
        pltp = PLTP.objects.get(sha1=pltp_sha1)
        strategy = Strategy.objects.get(name=strategy_name)
        activity = Activity(name=activity_name, pltp=pltp, strategy=strategy, id=activity_id)
        activity.save()
    
    request.session['current_activity'] = activity.name
    return HttpResponseRedirect(reverse(activity_view))

@login_required
def test_receiver(request, activity_name, strategy_name, pltp_sha1):
    try:
        activity = Activity.objects.get(name=activity_name)
    except:
        pltp = PLTP.objects.get(sha1=pltp_sha1)
        strategy = Strategy.objects.get(name=strategy_name)
        activity = Activity(name=activity_name, pltp=pltp, strategy=strategy, id=0)
        activity.save()
    request.session['current_activity'] = activity_name
    request.session['exercise'] = None
    return HttpResponseRedirect(reverse(activity_view))


@csrf_exempt
def try_pl(request, pl=None, warning=None):
    with evaluate(False):
        exercise = request.session.get('exercise', None)
    success = None
    feedback = None
    
    if pl:
        messages.success(request, "Le PL <b>"+pl.name+"</b> a bien été chargé.")
        messages.warning(request, warning)
    
    if not exercise:
        pl_dic = pl.json
        exercise = PythonBuilderTest(pl_dic).get_exercise()
    else:
        exercise = ExerciseTest(exercise)
    
    if request.method == 'GET' or request.method == 'POST':
        status = None
        try:
            status = json.loads(request.body.decode())
        except:
            pass
        if status and status['requested_action'] == 'submit' :
            success, feedback = exercise.evaluate(status['inputs'])
            return HttpResponse(json.dumps({'success': success, 'feedback': feedback}), content_type='application/json')
            
    request.session['exercise'] = exercise.dic
    return HttpResponse(exercise.render(request, feedback, success))
    
    
def not_authenticated(request):
    return render(request, 'playexo/not_authenticated.html', {})
    
